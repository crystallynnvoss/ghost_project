/*!
* Start Bootstrap - Grayscale v7.0.5 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

// window.addEventListener('DOMContentLoaded', event => {

//   // Navbar shrink function
//   var navbarShrink = function () {
//       const navbarCollapsible = document.body.querySelector('#mainNav');
//       if (!navbarCollapsible) {
//           return;
//       }
//       if (window.scrollY === 0) {
//           navbarCollapsible.classList.remove('navbar-shrink')
//       } else {
//           navbarCollapsible.classList.add('navbar-shrink')
//       }

//   };

//   // Shrink the navbar 
//   navbarShrink();

//   // Shrink the navbar when page is scrolled
//   document.addEventListener('scroll', navbarShrink);

//   // Activate Bootstrap scrollspy on the main nav element
//   const mainNav = document.body.querySelector('#mainNav');
//   if (mainNav) {
//       new bootstrap.ScrollSpy(document.body, {
//           target: '#mainNav',
//           offset: 74,
//       });
//   };

//   // Collapse responsive navbar when toggler is visible
//   const navbarToggler = document.body.querySelector('.navbar-toggler');
//   const responsiveNavItems = [].slice.call(
//       document.querySelectorAll('#navbarResponsive .nav-link')
//   );
//   responsiveNavItems.map(function (responsiveNavItem) {
//       responsiveNavItem.addEventListener('click', () => {
//           if (window.getComputedStyle(navbarToggler).display !== 'none') {
//               navbarToggler.click();
//           }
//       });
//   });

// });






document.getElementById("search").addEventListener("click", function(event){
  const searchValue = document.getElementById("search_term").value; {
    fetch("/search?location="+ searchValue)
      .then(response => response.json())
      .then(data => {
        document.querySelector("#locations").innerHTML=""
        for (const item of data){
        document.querySelector("#locations").insertAdjacentHTML("afterbegin", `<a href="/location/${item.id}"><li>${item.name}</li></a>`)
        //write a for loop to parse the response json onto the screen probably with insertAdjacentHTML onto #results
        }     
    });

  }
});

document.getElementById("map_search_button").addEventListener("click", function(event){
    const mapSearch = document.getElementById("map_search").value; {
      fetch("/search?location="+ mapSearch)
        .then(response => response.json())
        .then(data => {
            for (const searchvalue of data){
                longitude = searchvalue.longitude
                latitude = searchvalue.latitude
                createMarker(longitude, latitude)
        }     
    });

  }
});

mapboxgl.accessToken = 'pk.eyJ1IjoiZmlzaGVyMzQ3NCIsImEiOiJjbDFkcmQxNXMwazhpM21wNnNieTg4NWVqIn0.dmCThKx2-AVbtgD0bu3Pfw';
const map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [-122.446747, 37.733795],
zoom: 4
});


function createMarker(longitude, latitude){
    const marker1 = new mapboxgl.Marker()
    .setLngLat([longitude, latitude])
    .addTo(map);
}






