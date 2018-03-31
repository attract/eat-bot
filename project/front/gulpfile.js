var gulp 			= require('gulp');
var imagemin 		= require('gulp-imagemin');
var concat 			= require('gulp-concat');
var cssmin 			= require('gulp-minify-css');
var rename          = require('gulp-rename');
var less 			= require('gulp-less');
var sass 			= require('gulp-sass');
var copy            = require('gulp-contrib-copy');
var autoprefixer    = require('gulp-autoprefixer');
var helpers         = require('./gulp.helpers');
var minify          = require('gulp-babel-minify');
var uglify          = require('gulp-uglifyjs');


var PUBLIC_DIR = './../media';
var SRC_PATH   = 'src';
var path = {
    scripts : [ SRC_PATH+'/js/**/*.js' ],
    sass    : [ SRC_PATH+'/styles/style.scss' ],
    fonts   : [ SRC_PATH+'/fonts/**/*.*' ],
    img     : [ SRC_PATH+'/img/**/*.*' ]
};

require("any-promise/register")("bluebird");


gulp.task('fonts', function() {
    return gulp.src(path.fonts)
        .pipe(copy())
        .pipe(gulp.dest(PUBLIC_DIR+'/fonts'));
});

gulp.task('img', function() {
    return gulp.src(path.img)
        .pipe(imagemin())
        .pipe(copy())
        .pipe(gulp.dest(PUBLIC_DIR+'/img'));
});

gulp.task('script', function() {
    return helpers.es6toes5(SRC_PATH+'/js/index.js', 'app.js');
});

gulp.task('script-min', ['script'], function() {
    return gulp.src(PUBLIC_DIR+'/js/app.js')
        .pipe(minify({
            conditionals : false,
            evaluate     : false,
            unsafe       : false
        }))
        .pipe(gulp.dest(PUBLIC_DIR+'/js'));
});


gulp.task('js-min', function() {
    return gulp.src([SRC_PATH+'/js/landing/**/*.js'])
        .pipe(concat('landing.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(PUBLIC_DIR+'/js'));
});


gulp.task('sass', function() {
    return gulp.src(path.sass)
        .pipe(concat('style.min.css'))
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(cssmin())
        .pipe(gulp.dest(PUBLIC_DIR+'/css/front'));
});

// gulp.task('css-min', ['sass'], function() {
//     return gulp.src(SRC_PATH+'/styles/*.css')
//         .pipe(concat('style.css'))
//         .pipe(cssmin())
//         .pipe(rename({suffix: '.min'}))
//         .pipe(gulp.dest(PUBLIC_DIR+'/css/front'));
// });

gulp.task('watch', function() {
    gulp.watch(SRC_PATH+'/js/**/*.js', ['script']);
    gulp.watch(SRC_PATH+'/styles/**/*.scss', ['sass']);
});

gulp.task('default', ['js-min', 'sass', 'fonts', 'img', 'watch']);
gulp.task('prod', ['js-min', 'sass', /*'css-min',*/ 'fonts', 'img']);