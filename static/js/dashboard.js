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

async function updatePlanTable()
{
    const tableBody = document.getElementById("planTable");
    const clientID = 1;

    const response = await fetch(`/api/invest/get/plans`);
    const transData = await response.json();
    allPlans = transData;
        
    tableBody.innerHTML = "";
    transData.forEach(plan => {
        var id = plan.planID
        const planName = plan.planName
        
        if(plan.planID == 3)
            {
                plan.taxRate = `${plan.taxRate[0]*100} | ${plan.threshold[0]}<br>${plan.taxRate[1]*100} | ${plan.threshold[1]}`;
                plan.maxInvestYr = "Unlimited"
            }
        else
            {
                plan.taxRate = `${plan.taxRate*100} | ${plan.threshold}`
            }
        const row =`<tr data-id='${plan.planID}'>
                <td>${plan.planID}</td>
                <td>${plan.planName}</td>
                <td>${plan.desc}</td>
                <td>${plan.maxInvestYr}</td>
                <td>${plan.minLump}</td>
                <td>${plan.minMonthly}</td>
                <td>${plan.minReturnRate}</td>
                <td>${plan.maxReturnRate}</td>
                <td>${plan.taxRate}</td>
                <td>${plan.fee}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend",row);
    })

    
}
updatePlanTable();