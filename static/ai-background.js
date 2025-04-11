let neurons = [];
let NUM_NEURONS = 40;
let ACTIVATION_DISTANCE = 150;
let MAX_CONNECTIONS = 5;

function calculateDensity() {
    const screenArea = window.innerWidth * window.innerHeight;
    const baseDensity = 0.00004;
    NUM_NEURONS = Math.max(10, Math.floor(screenArea * baseDensity));
    ACTIVATION_DISTANCE = Math.min(150, Math.max(80, window.innerWidth / 10));
    MAX_CONNECTIONS = window.innerWidth < 768 ? 3 : 5;
}

function setup() {
    createCanvas(window.innerWidth, window.innerHeight);
    noFill();
    angleMode(DEGREES);
    calculateDensity();

    for (let i = 0; i < NUM_NEURONS; i++) {
        neurons.push(new Neuron());
    }
}

function drawGradientBackground(c1, c2) {
    noFill();
    for (let y = 0; y < height; y++) {
        let inter = map(y, 0, height, 0, 1);
        let c = lerpColor(c1, c2, inter);
        stroke(c);
        line(0, y, width, y);
    }
    noStroke();
}

function draw() {
    let color1 = color(240, 240, 240);  // Gris claro
    let color2 = color(230, 230, 230);  // Un tono ligeramente más oscuro
    drawGradientBackground(color1, color2);

    neurons.forEach(neuron => {
        neuron.update();
        neuron.show();
    });

    drawNeuralConnections();

    if (window.innerWidth > 768) {
        globalPulseEffect();
    }
}

class Neuron {
    constructor() {
        this.pos = createVector(random(width), random(height));
        this.connections = [];
        this.pulse = 0;
        const baseSize = window.innerWidth < 768 ? 6 : 8;
        this.targetSize = random(baseSize, baseSize * 1.8);
        this.hue = 210; // Azul oscuro
    }

    update() {
        const moveSpeed = window.innerWidth < 768 ? 0.2 : 0.3;
        this.pos.add(createVector(random(-moveSpeed, moveSpeed), random(-moveSpeed, moveSpeed)));
        this.pos.x = constrain(this.pos.x, 0, width);
        this.pos.y = constrain(this.pos.y, 0, height);

        let mouseDist = dist(mouseX, mouseY, this.pos.x, this.pos.y);
        if (mouseDist < ACTIVATION_DISTANCE) {
            this.activate();
        }

        this.pulse = lerp(this.pulse, 0, 0.1);
    }

    activate() {
        this.pulse = 1;
        this.hue = (this.hue + 1) % 360;
    }

    show() {
        let glowSize = this.targetSize * (1 + this.pulse * 2);
        let alpha = 150 + 105 * sin(frameCount * 0.1);

        fill(0, 51, 102, alpha * 0.5); // Azul oscuro
        noStroke();
        ellipse(this.pos.x, this.pos.y, glowSize);

        stroke(0, 51, 102, alpha); // Azul oscuro
        strokeWeight(window.innerWidth < 768 ? 1.5 : 2);
        fill(240, 240, 240); // Gris claro
        ellipse(this.pos.x, this.pos.y, this.targetSize);
    }
}

function drawNeuralConnections() {
  neurons.forEach((a, i) => {
      let others = neurons.slice(i + 1)
          .map(b => ({ neuron: b, dist: dist(a.pos.x, a.pos.y, b.pos.x, b.pos.y) }))
          .sort((x, y) => x.dist - y.dist)
          .slice(0, MAX_CONNECTIONS);

      others.forEach(({ neuron: b, dist }) => {
          if (dist < ACTIVATION_DISTANCE * 1.8) {
              // Mantener opacidad más consistente
              let alpha = map(dist, 0, ACTIVATION_DISTANCE * 1.8, 255, 50);
              
              // Líneas mucho más finas
              let lineWidth = map(dist, 0, ACTIVATION_DISTANCE * 1.8,
                  window.innerWidth < 768 ? 0.8 : 1.0,  // Reducido considerablemente
                  window.innerWidth < 768 ? 0.1 : 0.15); // Valores mínimos muy finos
              
              // Efecto de pulso reducido
              let pulseSpeed = window.innerWidth < 768 ? 0.02 : 0.03;
              let pulse = (sin(frameCount * pulseSpeed + dist * 0.01) + 1) * 0.3 + 0.7;
              alpha *= pulse;

              stroke(0, 51, 102, alpha);
              strokeWeight(lineWidth);
              line(a.pos.x, a.pos.y, b.pos.x, b.pos.y);
          }
      });
  });
}

function globalPulseEffect() {
    noFill();
    stroke(0, 51, 102, window.innerWidth < 768 ? 40 : 70); // Azul oscuro
    strokeWeight(window.innerWidth < 768 ? 1 : 1.5);
    let pulseSize = (frameCount % 120) * (window.innerWidth < 768 ? 3 : 4);
    ellipse(mouseX, mouseY, pulseSize, pulseSize);
}

function windowResized() {
    resizeCanvas(window.innerWidth, window.innerHeight);
    calculateDensity();
    neurons = [];
    for (let i = 0; i < NUM_NEURONS; i++) {
        neurons.push(new Neuron());
    }
} 