const URL = "http://127.0.0.1:5000/"


const app = Vue.createApp({ 
    data() {
        return {
            codigo: '',
            nombre: '',
            correo: '',
           // precio: '',
            //proveedor: '',
            //imagen_url: '',
            //imagenUrlTemp: null,
            mostrarDatosInscripto: false,
        };
    },


    methods: {
        obtenerInscripto() {
            fetch(URL + 'inscriptos/' + this.codigo)
                .then(response =>  {
                    if (response.ok) {
                        return response.json()
                    } else {
                        //Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.
                        throw new Error('Error al obtener los datos del inscripto.')
                    }
                })


                .then(data => {
                    this.nombre = data.nombre;
                    this.correo = data.correo;
                    //this.precio = data.precio;
                    //this.proveedor = data.proveedor;
                    //this.imagen_url =  data.imagen_url;
                    this.mostrarDatosInscripto = true;
                })
                .catch(error => {
                    console.log(error);
                    alert('Código no encontrado.');
                })
        },
        //seleccionarImagen(event) {
        //    const file = event.target.files[0];
        //    this.imagenSeleccionada = file;
        //    this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
        //},
        guardarCambios() {
            const formData = new FormData();
            formData.append('codigo', this.codigo);
            formData.append('nombre', this.nombre);
            formData.append('correo', this.correo);
            //formData.append('proveedor', this.proveedor);
            //formData.append('precio', this.precio);


            if (this.imagenSeleccionada) {
                formData.append('imagen', this.imagenSeleccionada, this.imagenSeleccionada.name);
            }


            //Utilizamos fetch para realizar una solicitud PUT a la API y guardar los cambios.
            fetch(URL + 'inscriptos/' + this.codigo, {
                method: 'PUT',
                body: formData,
            })
            .then(response => {
                //Si la respuesta es exitosa, utilizamos response.json() para parsear la respuesta en formato JSON.
                if (response.ok) {
                    return response.json()
                } else {
                    //Si la respuesta es un error, lanzamos una excepción.
                    throw new Error('Error al guardar los cambios del inscripto.')
                }
            })
            .then(data => {
                alert('Inscripto actualizado correctamente.');
                this.limpiarFormulario();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al actualizar el inscripto.');
            });
        },
        limpiarFormulario() {
            this.codigo = '';
            this.nombre = '';
            this.correo = '';
            //this.precio = '';
            //this.imagen_url = '';
            //this.imagenSeleccionada = null;
            //this.imagenUrlTemp = null;
            this.mostrarDatosInscripto = false;
        }
    }
});


app.mount('#app');
