let text = `Once upon a time in Eggville, lived a chicken named Cluck Norris...
He wore sunglasses at night and had over 2M followers on CluckTok.

But one thing haunted him: he never crossed the road...

UNTIL ONE DAY HE DID!`;

let index = 0;
let editor = document.getElementById('editor');
let message = document.getElementById('message');
let canvas = document.getElementById('volumeMeter');
let ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = 20;

function drawVolumeMeter(volume) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = volume > 0.5 ? 'red' : volume > 0.2 ? 'yellow' : 'green';
  ctx.fillRect(0, 0, volume * canvas.width, canvas.height);
}

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
.then(stream => {
  const audioCtx = new AudioContext();
  const mic = audioCtx.createMediaStreamSource(stream);
  const analyser = audioCtx.createAnalyser();
  mic.connect(analyser);

  const data = new Uint8Array(analyser.fftSize);

  function getVolume() {
    analyser.getByteTimeDomainData(data);
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
      let v = (data[i] - 128) / 128;
      sum += v * v;
    }
    return Math.sqrt(sum / data.length);
  }

  function loop() {
    const volume = getVolume();
    drawVolumeMeter(volume);

    if (volume > 0.05) {
      let speed = volume > 0.3 ? 5 : volume > 0.1 ? 2 : 1;
      message.innerText = "Yes! I hear your passion!";
      for (let i = 0; i < speed; i++) {
        if (index < text.length) {
          editor.innerText += text[index++];
        }
      }
    } else {
      message.innerText = "I can't hear your passion... scream louder!";
    }

    requestAnimationFrame(loop);
  }

  loop();
}).catch(err => {
  alert("Mic access is required. Please allow it.");
});
