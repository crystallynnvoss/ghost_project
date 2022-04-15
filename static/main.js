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






