// new window.IntaSend({
//     publicAPIKey: "ISPubKey_test_c35935db-78d3-4b6f-8ec3-221edb0abae1",
//     live: false //set to true when going live
//     })
//     .on("COMPLETE", (results) => console.log("Do something on success", results))
//     .on("FAILED", (results) => console.log("Do something on failure", results))
//     .on("IN-PROGRESS", (results) => console.log("Payment in progress status", results))

$(function() {
    var intaSend = new window.IntaSend({
        publicAPIKey: "ISPubKey_test_c35935db-78d3-4b6f-8ec3-221edb0abae1",
        live: false // Set to true when going live
    });

    $(intaSend)
        .on("COMPLETE", function(event, results) {
            console.log("Do something on success", results);
        })
        .on("FAILED", function(event, results) {
            console.log("Do something on failure", results);
        })
        .on("IN-PROGRESS", function(event, results) {
            console.log("Payment in progress status", results);
        });
});
