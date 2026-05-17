//Retrieve customer details from the api!!
var allUsers = [];
async function updateTable()
{
    const tableBody = document.getElementById("cusData");
    const clientID = 1;

    const response = await fetch(`/api/users/getsecure`);
    const transData = await response.json();
    allUsers = transData;
    tableBody.innerHTML = "";
    transData.forEach(user => {
        const row =`<tr data-id='${user.staffID}'>
                <td>${user.staffID}</td>
                <td>${user.firstName}</td>
                <td>${user.lastName}</td>
                <td>${user.email}</td>
                <td>${user.lastLogin}</td>
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
    const staffID = row.getAttribute("data-id");
    const user = allUsers.find(c => c.staffID == staffID);
    console.log(user)

    if (user)
        {
            const form = document.querySelector(".cusForm");

            form.querySelector("input[name='staffID']").value = user.staffID;
            form.querySelector('input[name="username"]').value = user.username;
            form.querySelector('input[name="firstName"]').value = user.firstName;
            form.querySelector('input[name="lastName"]').value = user.lastName;
            form.querySelector('input[name="email"]').value = user.email;
            form.querySelector('input[name="created"]').value = user.created;
            form.querySelector('input[name="lastLogin"]').value = user.lastLogin;
}});

//clear fields button
document.getElementById("clearButton").addEventListener("click", function(e)
{
    const previousSelected = document.querySelector(".selectedRow");
    if(previousSelected)
        {
            previousSelected.classList.remove("selectedRow");
        }
    
    const form = document.querySelector(".cusForm");

    form.querySelector("input[name='staffID']").value = "";
    form.querySelector('input[name="username"]').value = "";
    form.querySelector('input[name="firstName"]').value = "";
    form.querySelector('input[name="lastName"]').value = "";
    form.querySelector('input[name="email"]').value ="";
    form.querySelector('input[name="created"]').value = "";
    form.querySelector('input[name="lastLogin"]').value = "";
    form.querySelector('input[name="password"]').value = "";
    document.getElementById("message").innerText ="";
    });

// Modify Entry
document.getElementById("modButton").addEventListener("click",function()
{
    const form = document.querySelector(".cusForm");
    if(form.querySelector("input[name='staffID']").value == "")
        {
            return;
        }
    var staffID = form.querySelector('input[name="staffID"]').value;
    var username = form.querySelector('input[name="username"]').value;
    var firstName = form.querySelector('input[name="firstName"]').value;
    var lastName = form.querySelector('input[name="lastName"]').value;
    var email = form.querySelector('input[name="email"]').value;
    var password = form.querySelector('input[name="password"]').value;

    //DO THE API STUFF :)
    modifyUserAPI(staffID,username, firstName,lastName,email,password);
    updateTable();
})

async function modifyUserAPI(staffID, username, firstName,lastName,email, password)
{
    if (password == "")
        {
            password = null
        }
    const response = await fetch(`/api/users/modify/${staffID}/${username}/${firstName}/${lastName}/${encodeURIComponent(email)}/${password}`);
    const success = await response.json()
    if(success["success"] == true)
        {
            document.getElementById("message").innerText = "Successfully modified user entry!"
        }
    else
        {
            document.getElementById("message").innerText = "unsucessful modification of user entry!";
        }

}

document.getElementById("addButton").addEventListener("click",function()
{
    const form = document.querySelector(".cusForm");
    var staffID = form.querySelector('input[name="staffID"]').value;
    var username = form.querySelector('input[name="username"]').value;
    var firstName = form.querySelector('input[name="firstName"]').value;
    var lastName = form.querySelector('input[name="lastName"]').value;
    var email = form.querySelector('input[name="email"]').value;
    var password = form.querySelector('input[name="password"]').value;
    //DO THE API STUFF :)
    addUserAPI(username,firstName,lastName,email,password);
    updateTable();
})

async function addUserAPI(username,firstName,lastName,email,password)
{
    const response = await fetch(`/api/users/add/${username}/${firstName}/${lastName}/${encodeURIComponent(email)}/${password}`);
    const success = await response.json()
    if(success["success"] == true)
        {
            document.getElementById("message").innerText = "Successfully added new user!"
        }
    else
        {
            document.getElementById("message").innerText = "unsucessful addition of user";
        }

}