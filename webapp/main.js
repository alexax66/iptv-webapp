var playlist = [];
var currentChannel = 0;
var channelInput = "";
var inputTimeout;

function getQueryParameter() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.has('playlist') ? urlParams.get('playlist') : 'https://raw.githubusercontent.com/smolnp/IPTVru/gh-pages/IPTVmini.m3u';
}

function loadPlaylist(url) {
    console.log('Loading playlist from:', url);
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            console.log('Playlist data:', data);
            playlist = parseM3U(data);
            console.log('Parsed playlist:', playlist);
            playChannel(0); // Start with the first channel
        })
        .catch(error => console.error('Error loading playlist:', error));
}

function parseM3U(data) {
    let lines = data.split('\n');
    let channels = [];
    let channel = {};
    for (let line of lines) {
        if (line.startsWith('#EXTINF:')) {
            let info = line.split(',');
            channel.name = info[1].trim();
        } else if (line.startsWith('http')) {
            channel.url = line.trim();
            channels.push(channel);
            channel = {};
        }
    }
    return channels;
}

function playChannel(index) {
    if (index >= 0 && index < playlist.length) {
        currentChannel = index;
        let player = document.getElementById('player');
        let videoElement = document.createElement('video');
        videoElement.controls = true;
        videoElement.autoplay = true;

        if (Hls.isSupported()) {
            let hls = new Hls();
            hls.loadSource(playlist[index].url);
            hls.attachMedia(videoElement);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                videoElement.play();
            });
            hls.on(Hls.Events.ERROR, function(event, data) {
                console.error('Hls.js error:', data);
            });
        } else if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
            videoElement.src = playlist[index].url;
        } else {
            console.error('HLS not supported in this browser');
        }

        videoElement.addEventListener('error', function(event) {
            console.error('Error playing video:', event);
        });

        player.innerHTML = '';
        player.appendChild(videoElement);

        console.log('Playing channel:', playlist[index].name, 'URL:', playlist[index].url);
    } else {
        console.error('Invalid channel index:', index);
    }
}

function handleChannelInput(keyCode) {
    clearTimeout(inputTimeout);
    channelInput += (keyCode - 48).toString();

    if (channelInput.length >= 2) {
        let channelNumber = parseInt(channelInput, 10) - 1; // Adjust for zero-based index
        if (channelNumber >= 0 && channelNumber < playlist.length) {
            playChannel(channelNumber);
        } else {
            console.error('Channel number out of range:', channelNumber + 1);
        }
        channelInput = "";
    } else {
        inputTimeout = setTimeout(function() {
            let channelNumber = parseInt(channelInput, 10) - 1; // Adjust for zero-based index
            if (channelNumber >= 0 && channelNumber < playlist.length) {
                playChannel(channelNumber);
            } else {
                console.error('Channel number out of range:', channelNumber + 1);
            }
            channelInput = "";
        }, 1500);
    }
}

function changeChannel(delta) {
    let newChannel = (currentChannel + delta + playlist.length) % playlist.length;
    playChannel(newChannel);
}

document.addEventListener('keydown', function(event) {
    if (event.keyCode >= 48 && event.keyCode <= 57) { // Number keys
        handleChannelInput(event.keyCode);
    } else if (event.keyCode === 187) { // '+' key
        changeChannel(1);
    } else if (event.keyCode === 189) { // '-' key
        changeChannel(-1);
    }
});

window.onload = function() {
    let playlistURL = getQueryParameter();
    loadPlaylist(playlistURL);
};