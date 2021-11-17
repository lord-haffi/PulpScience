
const postMessage = self.postMessage;
let solver = undefined;

/**
 *
 * @param {Function} f
 * @param {Number[]} y0
 * @param {Number} t0
 * @param {Number} h
 * @param {{b:Number[], c:Number[], a:Number[][], dim:Number}} butcherTableau
 * @param {Number} fps
 * @constructor
 */
function ExplicitRungeKutta (f, y0, t0, h, butcherTableau, fps) {
    this.dim = y0.length;
    this.h = h;
    this.yi = y0.slice();
    this.ti = t0;
    this.phase = 0;
    this.postFreq = fps;
    this.butcherTableau = butcherTableau;
}

ExplicitRungeKutta.prototype = {
    frame: function () {
        while (this.phase < this.postFreq)
            this.step();
        this.phase -= this.postFreq;
        postMessage({ yi: this.yi, ti: this.ti });
    },
    step: function () {
        let yiNext = this.yi.slice();

        let k = [];
        for (let j = 0; j < this.butcherTableau.dim; j++){
            let yPuf = this.yi.slice();
            for (let l = 0; l < j; l++) {
                for (let n = 0; n < this.dim; n++) {
                    yPuf[n] += this.h * this.butcherTableau.a[j][l] * k [l][n];
                }
            }
            k[j] = this.f(this.ti + this.h * this.butcherTableau.c[j], yPuf);

            for (let n = 0; n < this.dim; n++) {
                yiNext[n] += this.h * this.butcherTableau.b[j] * k[j][n];
            }
        }

        this.yi = yiNext;
        this.ti += this.h;
        this.phase += this.h;
    }
};

self.addEventListener("message",
    /**
     *
     * @param {{data: {cmd:string}}} msg
     */
    function (msg) {
    switch (msg.data.cmd) {
        case "init":
            switch (msg.data.algorithm) {
                case "ExplicitRungeKutta":
                    importScripts(msg.data.fURL);
                    solver = new ExplicitRungeKutta(f, msg.data.y0, msg.data.t0, msg.data.h, msg.data.butcherTableau, msg.data.fps);
                    break;
                default:
                    throw "Unsupported solving algorithm: " + msg.data.algorithm;
            }
            break;
        case "nextFrame":
            if (solver)
                solver.frame();
            else
                throw "Solver is not initialized";
            break;
        default:
            throw "Invalid Command: " + msg.data.cmd;
    }
});
