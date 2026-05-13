let chart = null
document.getElementById("buttSub").disabled = true;
async function UpdateConversion() {
    const base = document.getElementById("baseCurr").value;
    const target = document.getElementById("conCurr").value;
    const amount = document.getElementById("baseAmount").value;
    const clientID = document.getElementById("customerName").value;

    // if (!amount || base === target) {
    //     document.getElementById("converted").innerText = "";
    //     return;
    // }
    console.log("FML")
    const response = await fetch(`/api/exchange/${base}/${target}/${amount}/${clientID}`);
    const data = await response.json();

    //console.log(response)
    document.getElementById("converted").innerText = `${amount} ${base} = ${data["convertedValue"]} ${target}\nFee: ${data["fee"]} GBP charged at ${data["tax"]}%\n FINAL AMOUNT: ${data["total"]} ${target}}`;
    updateTable()
}

//document.getElementById("baseCurr").addEventListener("change", updateConversion);
//document.getElementById("conCurr").addEventListener("change", updateConversion);
document.getElementById("baseAmount").addEventListener("input", function()
{
    var value = document.getElementById("baseAmount").value;
    var text = document.getElementById("converted");
    var customer = document.getElementById("customerName");
    if (value >=300 && value<=5000)
        {
            document.getElementById("buttSub").disabled = false;
            text.innerText = "";
        }
    else if (customer.value == 0)
        {
            document.getElementById("buttSub").disabled = true;
            text.innerText = "Must Select a Customer";
        }
    else
        {
            document.getElementById("buttSub").disabled =true;
            text.innerText = "Value entered is not within permissible range!\n min: 300 | max: 5000";
        } 
});

async function loadGraph(base,target)
{
    
    //var base = document.getElementById("baseCurr").value;
    //var target = document.getElementById("conCurr").value;
    var response = await fetch(`/api/history/${base}/${target}`);
    var data = await response.json();
    const graphobj = document.getElementById("historyGraph");
    chart = new Chart(graphobj, {
        type: "line",
        data: {
            labels: data.dates,
            datasets: [{
                label: `${base} → ${target}`,
                data: data.rates,
                borderColor: "blue",
                borderWidth: 2,
                fill: true,
                tension: 0.2,
                backgroundColor: 'rgba(59,130,246,0.1)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false }
            }
        }
    });
}

// Load default chart
loadGraph("USD", "GBP");

// Listen for changes
document.getElementById("baseCurr").addEventListener("change", () => {
    chart.destroy()
    var base = document.getElementById("baseCurr").value;
    var target = document.getElementById("conCurr").value;
    loadGraph(base, target);
});

document.getElementById("conCurr").addEventListener("change", () => {
    chart.destroy()
    var base = document.getElementById("baseCurr").value;
    var target = document.getElementById("conCurr").value;
    console.log(base,target);
    loadGraph(base, target);
});

//GET CUSTOMER DETAILS TO INJECT HERE!!
async function getCustomers() 
{
    const comboBox = document.getElementById("customerName");
    const response = await fetch("/api/customers/get/curr");
    const data = await response.json();
    console.log(data)
    

    data.clientID.forEach((id, index) => {
        const option = document.createElement("option");
        option.value = id;
        const firstName = data.firstName[index]
        const lastName = data.lastName[index]
        
        option.textContent = `${firstName} ${lastName}`;
        comboBox.appendChild(option);
        
    });

}
getCustomers();


async function updateTable()
{
    const selector = document.getElementById("customerName");
    const tableBody = document.getElementById("historyTable");
    const clientID = selector.value;
    console.log(selector.value)

    const response = await fetch(`/api/customers/get/currTrans/${clientID}`);
    const transData = await response.json();
    tableBody.innerHTML = "";
    transData.forEach(trans => {
        const row =`<tr>
                <td>${trans.transID}</td>
                <td>${trans.date}</td>
                <td>${trans.baseCurr}</td>
                <td>${trans.targetCurr}</td>
                <td>${trans.targetRate}</td>
                <td>${trans.startAmount}</td>
                <td>${trans.fee}</td>
                <td><strong>${trans.totalAmount.toLocaleString()}</strong></td>
            </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend",row);
    })

    
}
updateTable();

document.getElementById("customerName").value = 0;

document.getElementById("customerName").addEventListener("change", updateTable);

document.getElementById("customerName").addEventListener("change", function()
{
    if(document.getElementById("customerName").value == 0)
        {
            document.getElementById("buttSub").disabled = true
        }
});
