let babelify   = require('babelify');
let browserify = require('browserify');
let source = require('vinyl-source-stream');
let gulp = require('gulp');

let PUBLIC_DIR = './../media';

exports.es6toes5 = function (src, dest) {
    return browserify({entries: src, extensions: ['.js'], debug: true})
        .transform(babelify, {
            "presets": ["es2015"]
        })
        .bundle()
        .pipe(source(dest))
        .pipe(gulp.dest(PUBLIC_DIR+'/js'));
};

function fixPipe(stream) {
    let origPipe = stream.pipe;
    stream.pipe = function (dest) {
        arguments[0] = dest.on('error', function (error) {
            let nextStreams = dest._nextStreams;
            if (nextStreams) {
                nextStreams.forEach(function (nextStream) {
                    nextStream.emit('error', error);
                });
            } else if (dest.listeners('error').length === 1) {
                throw error;
            }
        });
        let nextStream = fixPipe(origPipe.apply(this, arguments));
        (this._nextStreams || (this._nextStreams = [])).push(nextStream);
        return nextStream;
    };
    return stream;
}

exports.fixPipe = fixPipe;