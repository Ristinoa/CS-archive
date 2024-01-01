/*
 * webapp.js
 * A.J. Ristino
 * 11 November, 2021
 */

/* NOTE: This is a very rough draft, mostly
 * based on the code by Professor Ondich.
 * For this reason, and for the reason that 
 * I'm not 100% sure on the syntax of how 
 * all of this works, there was some
 * guess and checking with prof. O's 
 * sample code.
 */
window.onload = initialize;

function initialize() {
    let element = document.getElementById('album_random');
    if (element) {
        element.onclick = onRandomAlbumChanged;
    }
    let element2 = document.getElementById('advsearch');
    if (element2) {
        element2.onclick = advsearchActivate;
    }
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port
        + '/api';
    return baseURL;
}

function onRandomAlbumChanged() {
   let url = getAPIBaseURL() + '/album/';

   fetch(url, { method: 'get' })
       .then((response) => response.json())
       .then(function (album) {
           let str = '';
           str += '<h2>' + album['ranking']
               + '</h2>' + '<p>' + album['artist']
               + ' | ' + album['name']
               + ' | ' + album['genres']
               + ' | ' + album['descs']
               + ' | ' + album['avrating']
               + ' | ' + album['numratings']
               + ' | ' + album['numreviews']
               + '</p>';
           let newHTML = document.getElementById('random_album');
           if (newHTML) {
                newHTML.innerHTML = str;
           }
       })
       .catch(function (error) {
            console.log(error);
        });
}
function advsearchActivate() {
    /* 
    This was painful.
    */

    let rankingLower = document.getElementById('ranking_lower').value;
    let rankingUpper = document.getElementById('ranking_upper').value;
    let artistName = document.getElementById('artist_name').value;
    let albumName = document.getElementById('album_name').value;
    let genres = document.getElementById('genres').value;
    let releaseYear = document.getElementById('release_year').value;
    let descs = document.getElementById('descs').value;
    let avratingLower = document.getElementById('avrating_lower').value;
    let avratingUpper = document.getElementById('avrating_upper').value;
    let numRatingLower = document.getElementById('numrating_lower').value;
    let numRatingUpper = document.getElementById('numrating_upper').value;
    let numReviewLower = document.getElementById('numreview_lower').value;
    let numReviewUpper = document.getElementById('numreview_upper').value;
    let url = getAPIBaseURL() + '/advsearch'
                + '?ranking_lower=' + rankingLower
                + '&ranking_upper=' + rankingUpper
                + '&artist_name=' + artistName
                + '&album_name=' + albumName
                + '&genres=' + genres
                + '&release_year=' + releaseYear
                + '&descs=' + descs
                + '&avrating_lower=' + avratingLower
                + '&avrating_upper=' + avratingUpper
                + '&numrating_lower=' + numRatingLower
                + '&numrating_upper=' + numRatingUpper
                + '&numreview_lower=' + numReviewLower
                + '&numreview_upper=' + numReviewUpper;

        fetch(url, {method: 'get'})

        .then((response) => response.json())

        .then(function(advsearch) {
             var tableBody='';
             for (var k = 0; k < advsearch.length; k++) {
                 tableBody += '<tr>';

                 tableBody += '<td>' + advsearch[k]['ranking'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['artist'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['name'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['genres'] + '/<td>';
                 tableBody += '<td>' + advsearch[k]['date'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['descs'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['avrating'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['numratings'] + '</td>';
                 tableBody += '<td>' + advsearch[k]['numreviews'] + '</td>';

                 tableBody += '</tr>';
                 
             }
             var resultsTableElement = document.getElementById('results_table');
             if (resultsTableElement) {
                 resultsTableElement.innerHTML = tableBody;
             }
         })
          .catch(function(error) {
             console.log(error);
         });
 
}

