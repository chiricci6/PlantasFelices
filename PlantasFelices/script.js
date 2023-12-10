const imagenSeguidora = document.getElementById('imagenSeguidora');

document.addEventListener('mousemove', (event) => {
  const mouseX = event.clientX + window.pageXOffset; // Coordenadas X del mouse con desplazamiento de página
  const mouseY = event.clientY + window.pageYOffset; // Coordenadas Y del mouse con desplazamiento de página

  // Mueve la imagen al cursor sin restricciones
  imagenSeguidora.style.left = mouseX + 'px';
  imagenSeguidora.style.top = mouseY + 'px';
});
var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validarFormulario() {
  var nombre = document.getElementById("nombre").value;
  var email = document.getElementById("email").value;
  var mensaje = document.getElementById("mensaje").value;
  
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  if (nombre === "" || mensaje === "") {
      alert("Por favor, complete todos los campos.");
      return false;
  } else if (!emailRegex.test(email)) {
      alert("Por favor, ingrese un correo electrónico válido.");
      return false;
  }
  return true;
}

