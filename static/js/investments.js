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
}

document.getElementById("generateQuote").addEventListener("click",function()
{
    validationCheck();
});