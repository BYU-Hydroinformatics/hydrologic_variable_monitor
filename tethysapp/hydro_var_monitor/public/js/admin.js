const App = (() => {
    'use strict';

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    ////////////////////////////////////////////////// DOM Elements
    const selectData = document.getElementById("select")
    const btnUpload = document.getElementById("upload-data")

    //btnSaveData.onclick = () => {
        //console.log(selectData.value)
    //}

    btnUpload.onclick = () => {
        console.log("uploading")
        //const exactJSONInput = document.getElementById("exact-json");
        //const simplifiedJSONInput = document.getElementById("simplified-json");
        const formData = new FormData();
        formData.append('exact-json', $('#exact-json')[0].files[0]);
        //const zipFile = zipFileInput.files[0];
        $.ajax({
            type: "POST", url: URL_UNZIP, data: formData, processData: false, contentType: false, success: data => {
                console.log(data)
            }
        })
    }

    ////////////////////////////////////////////////// Map and Map Layers

    return{}
})();
