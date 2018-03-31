/**
 * Created by DALEK on 26.01.2018.
 */
(function () {

    var slider = Peppermint(document.getElementById('peppermint'), {
        dots: true,
        slideshow: true,
        speed: 500,
        slideshowInterval: 30000,
        stopSlideshowAfterInteraction: false
    });


    // TOP-25 section

    // var ratingDisplay = document.querySelector(".rating__display");
    // var ratingSelect = document.querySelector(".rating__select");
    // var ratingOption = document.querySelectorAll(".rating__option");
    // var ratingSvg = document.querySelector(".rating__display svg");
    // var ratingSvgCode = '<svg width="21" height="13" viewBox="0 0 21 13" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>Back Arrow</title><desc>Created using Figma</desc><g id="Canvas1" transform="translate(4032 778)"><g id="Back Arrow"><g id="Back"><use xlink:href="#1path0_fill" transform="matrix(6.12323e-17 -1 1 6.12323e-17 -4031.76 -765.015)"/></g></g></g><defs><path id="1path0_fill" fill-rule="evenodd" d="M 11.9267 0.949552C 11.374 0.418975 10.5012 0.418975 9.94846 0.949552L 0 10.5L 9.94846 20.0504C 10.5012 20.581 11.374 20.581 11.9267 20.0504C 12.5123 19.4883 12.5123 18.5519 11.9267 17.9898L 4.12482 10.5L 11.9267 3.01025C 12.5123 2.44813 12.5123 1.51167 11.9267 0.949552Z"/></defs></svg>';
    //
    // ratingDisplay.addEventListener("click", function () {
    //     if (ratingSelect.classList.contains("rating__select--show")) {
    //         ratingSelect.classList.remove("rating__select--show");
    //         ratingDisplay.querySelector("svg").classList.remove("rating__display-svg--active");
    //     }
    //     else {
    //         ratingSelect.classList.add("rating__select--show");
    //         ratingDisplay.querySelector("svg").classList.add("rating__display-svg--active");
    //     }
    // });
    //
    // for (var i = 0; i < ratingOption.length; i++) {
    //     (function (ratingOption,i) {
    //         ratingOption[i].addEventListener("click", function () {
    //             ratingSelect.classList.remove("rating__select--show");
    //             ratingSvg.classList.remove("rating__display-svg--active");
    //             ratingDisplay.innerHTML = ratingOption[i].innerHTML + ratingSvgCode;
    //         });
    //     })(ratingOption,i);
    // }



    // var bestDisplay = document.querySelector(".best__display");
    // var bestSelect = document.querySelector(".best__select");
    // var bestOption = document.querySelectorAll(".best__option");
    // var bestSvgCode = '<svg width="25" height="16" viewBox="0 0 25 16" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>Back Arrow</title><desc>Created using Figma</desc><g id="Canvas" transform="translate(660 -1166)"><g id="Back Arrow"><g id="Back"><use xlink:href="#path0_fill" transform="matrix(6.12323e-17 -1 1 6.12323e-17 -660.669 1182)" fill="#00BF72"/></g></g></g><defs><path id="path0_fill" fill-rule="evenodd" d="M 14.5787 1.16069C 13.9031 0.512137 12.8361 0.512137 12.1606 1.16069L 0 12.8347L 12.1606 24.5088C 12.8361 25.1573 13.9031 25.1573 14.5787 24.5088C 15.2944 23.8217 15.2944 22.677 14.5787 21.9899L 5.042 12.8347L 14.5787 3.67959C 15.2944 2.99249 15.2944 1.84779 14.5787 1.16069Z"/></defs></svg>';
    //
    // bestDisplay.addEventListener("click", function () {
    //     if (bestSelect.classList.contains("best__select--show")) {
    //         bestSelect.classList.remove("best__select--show");
    //     }
    //     else {
    //         bestSelect.classList.add("best__select--show");
    //     }
    // });
    //
    // for (var i = 0; i < bestOption.length; i++) {
    //     (function (bestOption,i) {
    //         bestOption[i].addEventListener("click", function () {
    //             bestSelect.classList.remove("best__select--show");
    //             bestDisplay.innerHTML = bestOption[i].innerHTML + bestSvgCode;
    //         });
    //     })(bestOption,i);
    // }




    // var bestPeriodItems = document.querySelectorAll(".best__periods-item");
    // var bestPeriodItemActive = document.querySelector(".best__periods-item--active");
    //
    // for(var i=0; i<bestPeriodItems.length; i++) {
    //     (function(bestPeriodItems, i){
    //         bestPeriodItems[i].addEventListener("click", function () {
    //             if(!bestPeriodItems[i].classList.contains("best__periods-item--active")) {
    //                 bestPeriodItems[i].classList.add("best__periods-item--active");
    //                 bestPeriodItemActive.classList.remove("best__periods-item--active");
    //                 bestPeriodItemActive = bestPeriodItems[i];
    //             }
    //         })
    //     })(bestPeriodItems, i);
    // }

    // var ratingPeriodItems = document.querySelectorAll(".rating__periods-item");
    // var ratingPeriodItemActive = document.querySelector(".rating__periods-item--active");
    //
    // for(var i=0; i<ratingPeriodItems.length; i++) {
    //     (function(ratingPeriodItems, i){
    //         ratingPeriodItems[i].addEventListener("click", function () {
    //             if(!ratingPeriodItems[i].classList.contains("rating__periods-item--active")) {
    //                 ratingPeriodItems[i].classList.add("rating__periods-item--active");
    //                 ratingPeriodItemActive.classList.remove("rating__periods-item--active");
    //                 ratingPeriodItemActive = ratingPeriodItems[i];
    //             }
    //         })
    //     })(ratingPeriodItems, i);
    // }








})();