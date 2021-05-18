let map;

function initMap() {
  let lat = parseFloat(document.getElementById('latMap').value);
  let lng = parseFloat(document.getElementById('lngMap').value);
  let z = parseFloat(document.getElementById('zoomMap').value);
  const originalMapCenter = new google.maps.LatLng(lat, lng);
  map = new google.maps.Map(document.querySelector("#map"), {
    zoom: z,
    center: originalMapCenter,
    mapTypeId: 'satellite',
    disableDefaultUI: true,
  });

  initZoomControl(map);

  map.addListener("zoom_changed", () => {
    document.getElementById('zoomMap').value = map.getZoom();
  });

  map.addListener("center_changed", () => {
    document.getElementById('latMap').value = map.getCenter().lat();
    document.getElementById('lngMap').value = map.getCenter().lng();
  });
}

function updateMap() {
  let lat = parseFloat(document.getElementById('latMap').value);
  let lng = parseFloat(document.getElementById('lngMap').value);
  let newLatLng = new google.maps.LatLng(lat, lng);
  map.setCenter(newLatLng);
}

function initZoomControl(map) {
  document.querySelector(".zoom-control-in").onclick = function () {
    map.setZoom(map.getZoom() + 1);
  };

  document.querySelector(".zoom-control-out").onclick = function () {
    map.setZoom(map.getZoom() - 1);
  };
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(
    document.querySelector(".zoom-control")
  );
}
