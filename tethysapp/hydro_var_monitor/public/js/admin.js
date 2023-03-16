const App = (() => {
    'use strict';

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    ////////////////////////////////////////////////// DOM Elements
    //const selectData = document.getElementById("select")
    const btnUpload = document.getElementById("upload-data")
    const usrForm = document.getElementById("dir-name")
    const selectMang = document.getElementById('manage')
    const btnDelete = document.getElementById('delete-data')

    //btnSaveData.onclick = () => {
        //console.log(selectData.value)
    //}

    selectMang.innerHTML = `<option value="">Select a directory</option>${DIRECTORIES.map(src => `<option value="${src}">${src}</option>`).join("")}`;
    selectMang.onchange = () => {
        console.log("CHECL")
    }

    btnDelete.onclick = () =>{
        $('#lat-lon-modal').modal("show")
        console.log("click")
        const btnconfirmDelete = document.getElementById("confirm-delete")
        btnconfirmDelete.onclick = ()=> {
            console.log("deleting")
            $('#lat-lon-modal').modal("hide")
            const file_to_delete = selectMang.value
            console.log(file_to_delete)
            const delete_file = {
                "filename": file_to_delete
            }
            $.ajax({
                type: "GET", url: URL_DELETE, datatype: "JSON", data: delete_file, success: function (data){
                    console.log(data)
                }
            })
        }
    }

    btnUpload.onclick = () => {
        console.log("uploading")
        //const exactJSONInput = document.getElementById("exact-json");
        //const simplifiedJSONInput = document.getElementById("simplified-json");
        const formDataExact = new FormData();
        const formDataSimplified = new FormData();
        //how do I get the name of the directory into the file??
        formDataExact.append('exact-json', $('#exact-json')[0].files[0]);
        formDataSimplified.append('simplified-json', $('#simplified-json')[0].files[0]);
        //const zipFile = zipFileInput.files[0];
        $.ajax({
            type: "POST", url: URL_EXACT_UNZIP, data: formDataExact, processData: false, contentType: false, success: data => {
                console.log(data)
            }
        })
        $.ajax({
            type: "POST", url: URL_SIMPLIFIED_UNZIP, data: formDataSimplified, processData: false, contentType: false, success: data => {
                console.log(data)
            }
        })
    }

    ////////////////////////////////////////////////// Map and Map Layers

    return{}
})();
