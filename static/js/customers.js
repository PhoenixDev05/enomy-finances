//Retrieve customer details from the api!!
var allCustomers = [];
async function updateTable()
{
    const tableBody = document.getElementById("cusData");
    const clientID = 1;

    const response = await fetch(`/api/customers/get/all`);
    const transData = await response.json();
    allCustomers = transData;
    tableBody.innerHTML = "";
    transData.forEach(cus => {
        const row =`<tr data-id='${cus.clientID}'>
                <td>${cus.clientID}</td>
                <td>${cus.firstName}</td>
                <td>${cus.lastName}</td>
                <td>${cus.phone}</td>
                <td>${cus.email}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend",row);
    })

    
}
updateTable();

//Loading the customer info into the fields
document.getElementById("cusData").addEventListener("click", function(e)
{
    const row = e.target.closest("tr");
    if(!row) return;

    const previousSelected = document.querySelector(".selectedRow");
    if(previousSelected)
        {
            previousSelected.classList.remove("selectedRow");
        }
    
    row.classList.add("selectedRow")
    const clientID = row.getAttribute("data-id");
    const customer = allCustomers.find(c => c.clientID == clientID);
    console.log(customer)

    if (customer)
        {
            const form = document.querySelector(".cusForm");

            form.querySelector("input[name='cusID']").value = customer.clientID;
            form.querySelector('input[name="firstName"]').value = customer.firstName;
            form.querySelector('input[name="lastName"]').value = customer.lastName;
            form.querySelector('input[name="email"]').value = customer.email;
            form.querySelector('input[name="phoneNum"]').value = customer.phone;
            form.querySelector('input[name="addressLine1"]').value = customer.addressLine1;
            form.querySelector('input[name="addressLine2"]').value = customer.addressLine2;
            form.querySelector('input[name="city"]').value = customer.city;
            form.querySelector('input[name="postcode"]').value = customer.postcode;
            form.querySelector('input[name="country"]').value = customer.country;
        }
});

//clear fields button
document.getElementById("clearButton").addEventListener("click", function(e)
{
    const previousSelected = document.querySelector(".selectedRow");
    if(previousSelected)
        {
            previousSelected.classList.remove("selectedRow");
        }
    
    const form = document.querySelector(".cusForm");

    form.querySelector("input[name='cusID']").value = "";
    form.querySelector('input[name="firstName"]').value = ""
    form.querySelector('input[name="lastName"]').value = "";
    form.querySelector('input[name="email"]').value = "";
    form.querySelector('input[name="phoneNum"]').value = "";
    form.querySelector('input[name="addressLine1"]').value = "";
    form.querySelector('input[name="addressLine2"]').value = "";
    form.querySelector('input[name="city"]').value = "";
    form.querySelector('input[name="postcode"]').value = "";
    form.querySelector('input[name="country"]').value = "";
    document.getElementById("message").innerText ="";
    });

// Modify Entry
document.getElementById("modButton").addEventListener("click",function()
{
    const form = document.querySelector(".cusForm");
    if(form.querySelector("input[name='cusID']").value == "")
        {
            return;
        }
    var clientID = form.querySelector('input[name="cusID"]').value;
    var firstName = form.querySelector('input[name="firstName"]').value;
    var lastName = form.querySelector('input[name="lastName"]').value;
    var email = form.querySelector('input[name="email"]').value;
    var phone = form.querySelector('input[name="phoneNum"]').value;
    var addr1 = form.querySelector('input[name="addressLine1"]').value;
    var addr2 = form.querySelector('input[name="addressLine2"]').value;
    var city = form.querySelector('input[name="city"]').value;
    var postcode = form.querySelector('input[name="postcode"]').value;
    var country = form.querySelector('input[name="country"]').value;

    //DO THE API STUFF :)
    modifyCustomerAPI(clientID,firstName,lastName,email,phone,addr1,addr2,city,postcode,country);
})

async function modifyCustomerAPI(clientID, firstName,lastName,email,phone,addr1,addr2,city,postcode,country)
{
    if (addr2 == "")
        {
            addr2 = null;
        }
    const response = await fetch(`/api/customers/modify/${clientID}/${firstName}/${lastName}/${encodeURIComponent(email)}/${phone}/${encodeURIComponent(addr1)}/${encodeURIComponent(addr2)}/${city}/${encodeURIComponent(postcode)}/${encodeURIComponent(country)}`);
    const success = await response.json()
    if(success["success"] == true)
        {
            document.getElementById("message").innerText = "Successfully modified customer entry!"
        }
    else
        {
            document.getElementById("message").innerText = "unsucessful modification of customer entry!";
        }

}