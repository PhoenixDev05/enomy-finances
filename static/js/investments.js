async function updatePlanTable()
{
    const tableBody = document.getElementById("planTable");
    const clientID = 1;

    const response = await fetch(`/api/invest/get/plans`);
    const transData = await response.json();
    allPlans = transData;
    const planCombo = document.getElementById("planCombo")
        
    tableBody.innerHTML = "";
    transData.forEach(plan => {
        var id = plan.planID
        const option = document.createElement("option");
        option.value = id;
        const planName = plan.planName
        
        option.textContent = `${planName}`;
        planCombo.appendChild(option);
        if(plan.planID == 3)
            {
                plan.taxRate = `${plan.taxRate[0]} | ${plan.threshold[0]}<br>${plan.taxRate[1]} | ${plan.threshold[1]}`;
                plan.maxInvestYr = "Unlimited"
            }
        else
            {
                plan.taxRate = `${plan.taxRate} | ${plan.threshold}`
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

async function validationCheck()
{
    const planID = document.getElementById("planCombo").value;
    const initialAmount = document.getElementById("initialAmount").value;
    const monthlyAmount = document.getElementById("monthlyAmount").value

    const response = await fetch(`/api/invest/validate/${planID}/${initialAmount}/${monthlyAmount}`);
    const data = await response.json()
    if (data["success"] != true)
        {
            document.getElementById("message").innerText = data["message"];
        }
    else
        {
            console.log("YAY")
            generateQuote();
        }
}

async function generateQuote()
{
    const clientID = document.getElementById("customerName").value;
    const planID = document.getElementById("planCombo").value;
    const initialAmount = document.getElementById("initialAmount").value;
    const monthlyAmount = document.getElementById("monthlyAmount").value;
    
    const response = await fetch(`/api/invest/quote/${clientID}/${planID}/${initialAmount}/${monthlyAmount}`);
    const data = await response.json();
    console.log(data);
    updateQuoteTable();
}

async function updateQuoteTable()
{
document.getElementById("tableData").innerHTML = "";
const clientID = document.getElementById("customerName").value;
const response = await fetch(`/api/invest/get/quote/${clientID}`);
const data = await response.json();
console.log(data);

let highestProfit = -1;

for (const quote of data) {
    const year10 = quote.projections?.find(p => p.year === 10);
    const maxReturnData = year10?.returns?.find(r => r.type === 'max');
    const maxProfit = maxReturnData?.profit || 0;
    
    quote.calculatedMaxProfit = maxProfit; 
    
    if (maxProfit > highestProfit) {
        highestProfit = maxProfit;
    }
}

data.sort((a, b) => b.calculatedMaxProfit - a.calculatedMaxProfit);

for (const quote of data) {
    const getYearData = (yearNum) => {
        const proj = quote.projections.find(p => p.year === yearNum);
        if (!proj) return { min: {}, max: {} };

        const minData = proj.returns.find(r => r.type === 'min') || {};
        const maxData = proj.returns.find(r => r.type === 'max') || {};
        return { min: minData, max: maxData };
    }
    
    const y1 = getYearData(1);
    const y5 = getYearData(5);
    const y10 = getYearData(10);

    const isRecommended = quote.calculatedMaxProfit === highestProfit && highestProfit > 0;
    const rowClass = isRecommended ? 'class="recommended"' : '';
    const badge = isRecommended ? '<span style="color: #0f5132; font-weight: bold; display: block; font-size: 0.75rem; margin-top: 4px;">★ Recommended</span>' : '';

    const rowHTML = `
        <tr ${rowClass}>
            <td>
                ${quote.dateMade}
                ${badge}
            </td>
           
            <td>£${quote.initialAmount.toFixed(2)}</td>
            <td>£${quote.monthlyAmount.toFixed(2)}</td>
            <td>
                ${quote.planID}
            </td>
             

            <td>£${(y1.min.return || 0).toFixed(2)}</td>
            <td>£${(y1.max.return || 0).toFixed(2)}</td>
            <td>£${(y1.min.profit || 0).toFixed(2)}</td>
            <td>£${(y1.max.profit || 0).toFixed(2)}</td>
            <td>£${(y1.min.fees || 0).toFixed(2)}</td>
            <td>£${(y1.min.tax || 0).toFixed(2)}</td>
            <td>£${(y1.max.tax || 0).toFixed(2)}</td>

            <td>£${(y5.min.return || 0).toFixed(2)}</td>
            <td>£${(y5.max.return || 0).toFixed(2)}</td>
            <td>£${(y5.min.profit || 0).toFixed(2)}</td>
            <td>£${(y5.max.profit || 0).toFixed(2)}</td>
            <td>£${(y5.min.fees || 0).toFixed(2)}</td>
            <td>£${(y5.min.tax || 0).toFixed(2)}</td>
            <td>£${(y5.max.tax || 0).toFixed(2)}</td>

            <td>£${(y10.min.return || 0).toFixed(2)}</td>
            <td>£${(y10.max.return || 0).toFixed(2)}</td>
            <td>£${(y10.min.profit || 0).toFixed(2)}</td>
            <td>£${(y10.max.profit || 0).toFixed(2)}</td>
            <td>£${(y10.min.fees || 0).toFixed(2)}</td>
            <td>£${(y10.min.tax || 0).toFixed(2)}</td>
            <td>£${(y10.max.tax || 0).toFixed(2)}</td>
        </tr>
    `;
    document.getElementById("tableData").insertAdjacentHTML('beforeend', rowHTML);
}
};
updateQuoteTable();

document.getElementById("customerName").addEventListener("change" ,function()
{
    updateQuoteTable();
})



document.getElementById("generateQuote").addEventListener("click",function()
{
    validationCheck();
});

//input validation checkers
document.getElementById("customerName").addEventListener("change",function(){
    const value = document.getElementById("customerName").value
    if(value <1){
        document.getElementById("generateQuote").disabled = true;
    }
    else{
        document.getElementById("generateQuote").disabled = false;
    }
})
document.getElementById("generateQuote").disabled = true;