const imagenSeguidora = document.getElementById('imagenSeguidora');

document.addEventListener('mousemove', (event) => {
  const mouseX = event.clientX + window.pageXOffset; // Coordenadas X del mouse con desplazamiento de página
  const mouseY = event.clientY + window.pageYOffset; // Coordenadas Y del mouse con desplazamiento de página

  // Mueve la imagen al cursor sin restricciones
  imagenSeguidora.style.left = mouseX + 'px';
  imagenSeguidora.style.top = mouseY + 'px';
});
