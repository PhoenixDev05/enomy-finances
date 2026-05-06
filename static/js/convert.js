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
    document.getElementById("converted").innerText = `${amount} ${base} = ${data["convertedValue"]} ${target}\nFee: ${data["fee"]} GBP charged at ${data["tax"]}%`;
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
