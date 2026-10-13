let notas = document.querySelectorAll(".nota");

notas.forEach(function(td) {
    if (parseFloat(td.textContent) >= 5) {
        td.style.backgroundColor = "green";
    } else {
        td.style.backgroundColor = "red";
    }
});
