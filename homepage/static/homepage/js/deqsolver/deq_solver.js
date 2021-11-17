
const DEQ = {
    Explicit
};

// function extend (child, parent) {
//     let constructor = child.prototype.constructor;
//     child.prototype = Object.create(parent.prototype);
//     child.prototype.constructor = constructor;
// }

function FrameQueue (maxDeadElements=1024) {
    this.data = [];
    this.count = 0;
    this.offset = 0;
    this.maxPoll = maxDeadElements;
}
FrameQueue.prototype = {
    push: function (element) {
        this.data[this.offset + this.count++] = element;
    },
    peek: function () {
        return this.data[this.offset];
    },
    poll: function () {
        let ret = this.data[this.offset++];
        if (this.offset * 2 > this.count || this.offset > this.maxPoll) {
            this.data = this.data.slice(this.offset);
            this.offset = 0;
        }
        this.count--;
        return ret;
    }
}

// function LimitedFrameQueue(size) {
//     this.data = [];
//     this.count = 0;
//     this.offset = 0;
//     this.size = size;
// }
// LimitedFrameQueue.prototype = {
//     push: function (element) {
//         this.data[this.offset + this.count++] = element;
//         if (this.count > this.size) {
//             this.poll();
//         }
//     },
//     peek: function () {
//         return this.data[this.offset];
//     },
//     poll: function () {
//         let ret = this.data[this.offset++];
//         if (this.offset * 2 > this.count) {
//             this.data = this.data.slice(this.offset);
//             this.offset = 0;
//         }
//         this.count--;
//         return ret;
//     }
// };

function BlockingFrameQueue(size) {
    
}
