let chart = null

async function UpdateConversion() {
    const base = document.getElementById("baseCurr").value;
    const target = document.getElementById("conCurr").value;
    const amount = document.getElementById("baseAmount").value;

    // if (!amount || base === target) {
    //     document.getElementById("converted").innerText = "";
    //     return;
    // }
    console.log("FML")
    const response = await fetch(`/api/exchange/${base}/${target}/${amount}`);
    const data = await response.json();

    //console.log(response)
    document.getElementById("converted").innerText = `${amount} ${base} = ${data["convertedValue"]} ${target}\nFee: ${data["fee"]} USD charged at ${data["tax"]}%\n FINAL AMOUNT: ${data["total"]} ${target}}`;
}

//document.getElementById("baseCurr").addEventListener("change", updateConversion);
//document.getElementById("conCurr").addEventListener("change", updateConversion);
document.getElementById("baseAmount").addEventListener("input", function()
{
    var value = document.getElementById("baseAmount").value;
    var text = document.getElementById("converted")
    if (value >=300 && value<=5000)
        {
            document.getElementById("buttSub").disabled = false;
            text.innerText = "";
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
                fill: false,
                tension: 0.2
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