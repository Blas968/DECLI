const dias = [
  "domingo",
  "lunes",
  "martes",
  "miércoles",
  "jueves",
  "viernes",
  "sábado"
];

const meses = [
  "enero",
  "febrero",
  "marzo",
  "abril",
  "mayo",
  "junio",
  "julio",
  "agosto",
  "septiembre",
  "octubre",
  "noviembre",
  "diciembre"
];

const hoy = new Date();

function diasHasta(fecha) {
  const diferenciaMs = new Date(fecha) - new Date();
  return Math.ceil(diferenciaMs / 86400000);
}

console.log(`${dias[hoy.getDay()]}, ${hoy.getDate()} de ${meses[hoy.getMonth()]} de ${hoy.getFullYear()}`);

const miCumpleanos = new Date(2027, 8, 15);
console.log(`Faltan ${diasHasta(miCumpleanos)} días para mi cumpleaños.`);
