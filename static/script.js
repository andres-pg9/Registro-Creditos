const API_URL = "http://127.0.0.1:5000/creditos";
const form = document.getElementById("creditoForm");
const tabla = document.querySelector("#tablaCreditos tbody");
let graficaCreditos = null;
let graficaClientes = null;
let graficaRangos = null;

// ------------------ REGISTRAR CRÉDITO ------------------
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    
    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        
        // Verificar si la respuesta es exitosa
        if (res.ok) {
            console.log("Crédito registrado exitosamente"); // Debug
            form.reset();
            
            // Recargar datos
            await cargarCreditos();
            await cargarGraficaEvolucion();
            await cargarGraficaClientes();
            await cargarGraficaRangos();
            
            // Mostrar modal de éxito - CORREGIDO
            const modalExito = new bootstrap.Modal(document.getElementById("modalExito"));
            modalExito.show();
        } else {
            // Manejar errores de respuesta
            console.error("Error en la respuesta:", res.status, res.statusText);
            const errorText = await res.text();
            console.error("Detalle del error:", errorText);
        }
    } catch (err) {
        console.error("Error al registrar crédito:", err);
        // Mostrar un mensaje de error al usuario
        alert("Error al registrar el crédito. Por favor, inténtalo de nuevo.");
    }
});

// ------------------ LISTAR CRÉDITOS ------------------
async function cargarCreditos() {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const creditos = await res.json();
        
        tabla.innerHTML = "";
        creditos.forEach((c) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${c.id}</td>
                <td>${c.cliente}</td>
                <td>${c.monto}</td>
                <td>${c.tasa_interes}</td>
                <td>${c.plazo}</td>
                <td>${c.fecha_otorgamiento}</td>
                <td>
                    <button class="btn btn-editar" onclick="editarCredito(${c.id})">Editar</button>
                    <button class="btn btn-danger" onclick="eliminarCredito(${c.id})">Eliminar</button>
                </td>
            `;
            tabla.appendChild(row);
        });
    } catch (err) {
        console.error("Error al cargar créditos:", err);
    }
}

// ------------------ ELIMINAR CRÉDITO ------------------
async function eliminarCredito(id) {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const creditos = await res.json();
        const credito = creditos.find(c => c.id === id);
        
        if (!credito) return;

        // Llenar datos en el modal
        document.getElementById("deleteId").value = credito.id;
        document.getElementById("mensajeEliminar").innerText = 
            `¿Seguro que deseas eliminar el crédito #${credito.id} del cliente ${credito.cliente}?`;

        // Mostrar modal
        const modalEliminar = new bootstrap.Modal(document.getElementById("eliminarModal"));
        modalEliminar.show();
    } catch (err) {
        console.error("Error al preparar eliminación:", err);
    }
}

document.getElementById("btnConfirmarEliminar").addEventListener("click", async () => {
    const id = document.getElementById("deleteId").value;
    try {
        const res = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });
        
        if (res.ok) {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById("eliminarModal"));
            if (modalInstance) {
                modalInstance.hide();
            }
            await cargarCreditos();
            await cargarGraficaEvolucion();
            await cargarGraficaClientes();
            await cargarGraficaRangos();
        }
    } catch (err) {
        console.error("Error al eliminar crédito:", err);
    }
});

// ------------------ EDITAR CRÉDITO (MODAL) ------------------
async function editarCredito(id) {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const creditos = await res.json();
        const creditoActual = creditos.find((c) => c.id === id);

        if (!creditoActual) return;

        // Llenar modal
        document.getElementById("editId").value = creditoActual.id;
        document.getElementById("editCliente").value = creditoActual.cliente;
        document.getElementById("editMonto").value = creditoActual.monto;
        document.getElementById("editTasa").value = creditoActual.tasa_interes;
        document.getElementById("editPlazo").value = creditoActual.plazo;
        document.getElementById("editFecha").value = creditoActual.fecha_otorgamiento;

        // Mostrar modal
        const modalEditar = new bootstrap.Modal(document.getElementById("editarModal"));
        modalEditar.show();
    } catch (err) {
        console.error("Error al cargar crédito para edición:", err);
    }
}

// Guardar cambios desde el modal
document.getElementById("editarForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const id = document.getElementById("editId").value;
    const data = {
        cliente: document.getElementById("editCliente").value,
        monto: parseFloat(document.getElementById("editMonto").value),
        tasa_interes: parseFloat(document.getElementById("editTasa").value),
        plazo: parseInt(document.getElementById("editPlazo").value),
        fecha_otorgamiento: document.getElementById("editFecha").value,
    };

    try {
        const res = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (res.ok) {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById("editarModal"));
            if (modalInstance) {
                modalInstance.hide();
            }
            await cargarCreditos();
            await cargarGraficaEvolucion();
            await cargarGraficaClientes();
            await cargarGraficaRangos();
        } else {
            console.error("Error al actualizar:", res.status, res.statusText);
        }
    } catch (err) {
        console.error("Error al actualizar crédito:", err);
    }
});

// ------------------ GRÁFICA EVOLUCIÓN ------------------
async function cargarGraficaEvolucion() {
    try {
        const res = await fetch(`${API_URL}`);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const creditos = await res.json();

        // Agrupar por mes y calcular totales
        const montosPorMes = {};
        let total = 0;
        const clientesSet = new Set();

        creditos.forEach(c => {
            const mes = c.fecha_otorgamiento.slice(0, 7); // YYYY-MM
            montosPorMes[mes] = (montosPorMes[mes] || 0) + c.monto;
            total += c.monto;
            clientesSet.add(c.cliente);
        });

        // Actualizar tarjetas
        document.getElementById("montoTotal").innerText = `$${total.toLocaleString("es-MX")}`;
        document.getElementById("totalClientes").innerText = clientesSet.size;
        document.getElementById("totalCreditos").innerText = creditos.length;

        // Gráfica de evolución
        const labels = Object.keys(montosPorMes);
        const valores = Object.values(montosPorMes);
        const ctx = document.getElementById("graficaEvolucion").getContext("2d");

        // Destruir gráfica anterior si existe
        if (graficaCreditos) {
            graficaCreditos.destroy();
        }

        graficaCreditos = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Monto otorgado por mes",
                    data: valores,
                    borderColor: "rgba(54, 162, 235, 0.8)",
                    backgroundColor: "rgba(54, 162, 235, 0.3)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (err) {
        console.error("Error al cargar gráfica de evolución:", err);
    }
}

async function cargarGraficaClientes() {
    try {
        const res = await fetch(`http://127.0.0.1:5000/creditos/por_cliente`);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const data = await res.json();

        const labels = data.map(d => d.cliente);
        const valores = data.map(d => d.total);

        // Actualizar tarjetas
        document.getElementById("cardClientes").innerText = labels.length;
        const promedio = valores.length > 0 ? valores.reduce((a, b) => a + b, 0) / labels.length : 0;
        document.getElementById("promedioCliente").innerText = `${promedio.toLocaleString("es-MX")}`;

        // Destruir gráfica anterior si existe
        if (graficaClientes) {
            graficaClientes.destroy();
        }

        // Crear gráfica
        const ctx = document.getElementById("graficaClientes").getContext("2d");
        graficaClientes = new Chart(ctx, {
            type: "pie",
            data: {
                labels,
                datasets: [{
                    label: "Créditos por Cliente",
                    data: valores,
                    backgroundColor: [
                        "#36A2EB", "#FF6384", "#4CAF50", "#FFC107", 
                        "#9C27B0", "#00BCD4", "#E91E63"
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "right" }
                }
            }
        });
    } catch (err) {
        console.error("Error al cargar gráfica de clientes:", err);
    }
}

async function cargarGraficaRangos() {
    try {
        const res = await fetch(`http://127.0.0.1:5000/creditos/por_rangos`);
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        const data = await res.json();

        const labels = Object.keys(data);
        const valores = Object.values(data);

        // Destruir gráfica anterior si existe
        if (graficaRangos) {
            graficaRangos.destroy();
        }

        const ctx = document.getElementById("graficaRangos").getContext("2d");
        graficaRangos = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels,
                datasets: [{
                    label: "Distribución por Rango",
                    data: valores,
                    backgroundColor: ["#2196F3", "#FF9800", "#F44336"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    } catch (err) {
        console.error("Error al cargar gráfica de rangos:", err);
    }
}

// ------------------ INICIO ------------------
document.addEventListener("DOMContentLoaded", async () => {
    console.log("Cargando aplicación..."); // Debug
    try {
        await cargarCreditos();
        await cargarGraficaEvolucion();
        await cargarGraficaClientes();
        await cargarGraficaRangos();
        console.log("Aplicación cargada correctamente"); // Debug
    } catch (err) {
        console.error("Error al inicializar aplicación:", err);
    }
});