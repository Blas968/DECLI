const libro = {
    titulo: "Ayu",
    autor: "aayu",
    paginas: 300,
    resumen(){
        for (const dato in libro){
            console.log(`${dato}: ${libro[dato]}`)
        }
        console.log(libro.resumen())
    }
}

const producto = {
    nombre: "alcachofa",
    precio: 12,
    stock: 200,
    conIva(){
        return this.precio * 1.21
    },
    vender(n){
        if(this.stock >= n){
            this.stock = this.stock-n
            return true
        }else{
            return false
        }
    }
}

const alcachofa = { nombre: "alcachofa", precio: 12, stock: 200 }
const manzana = { nombre: "manzana", precio: 3, stock: 4 }
const pan = { nombre: "pan", precio: 2.5, stock: 7 }
const leche = { nombre: "leche", precio: 1.8, stock: 2 }

const productos = [alcachofa, manzana, pan, leche]

const productosBajoStock = productos.filter(producto => producto.stock < 5)
console.log("Productos con menos de 5 unidades:")
console.log(productosBajoStock)

const totalInventario = productos.reduce((total, producto) => total + (producto.precio * producto.stock), 0)
console.log(`Valor total del inventario: ${totalInventario}`)

