//const URL = "http://127.0.0.1:5000/"
const URL = "https://fedelaza.pythonanywhere.com/"


const app = Vue.createApp({
    data() {
        return {
            inscriptos: []
        }
    },
    methods: {
        obtenerInscriptos() {
            // Obtenemos el contenido del inventario
            fetch(URL + 'inscriptos')
                .then(response => {
                    // Parseamos la respuesta JSON
                    if (response.ok) { return response.json(); }
                })
                .then(data => {
                    // El código Vue itera este elemento para generar la tabla
                    this.inscriptos = data;
                })
                .catch(error => {
                    console.log('Error:', error);
                    alert('Error al obtener los inscriptos.');
                });
        },
        eliminarInscripto(codigo) {
            if (confirm('¿Estás seguro de que quieres eliminar este inscripto?')) {
                fetch(URL + `inscriptos/${codigo}`, { method: 'DELETE' })
                    .then(response => {
                        if (response.ok) {
                            this.inscriptos = this.inscriptos.filter(inscripto => inscripto.codigo !== codigo);
                            alert('Inscripto eliminado correctamente.');
                        }
                    })
                    .catch(error => {
                        alert(error.message);
                    });
            }
        }
    },
    mounted() {
        //Al cargar la página, obtenemos la lista de inscriptos
        this.obtenerInscriptos();
    }
});
app.mount('body');
