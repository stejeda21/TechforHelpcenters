// Search filter
$(document).ready(function() {
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


// Method for adjusting help center capacity
let value = 0;
progress = document.getElementById("progress");
percentage = document.getElementById("percentage");
refugeeData = document.getElementById("refugee-data")
status = document.getElementById("status").innerHTML;
// console.log(status);

function increaseCapacity() {
    if (status === "checked in") {
        value = value + 25;
        if (value >= 100)
            progress.style.width = value + "%";
        percentage.innerHTML = value + "%";

    }
}

function decreaseCapacity() {
    if (status === "checked out") {
        value = value - 25;
        if (value <= 0)
            value = 0;
        progress.style.width = value + "%";
        percentage.innerHTML = value + "%";
    }

}

status.append(increaseCapacity());
status.append(decreaseCapacity());