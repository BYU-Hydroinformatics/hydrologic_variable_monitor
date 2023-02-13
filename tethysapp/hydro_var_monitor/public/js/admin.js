const App = (() => {
    'use strict';

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    ////////////////////////////////////////////////// DOM Elements
    const selectData = document.getElementById("select")
    const btnSaveData = document.getElementById("save-data")
    const btnUploadData = document.getElementById("upload-data")
    const btnUpload = document.getElementById("upload")

    btnSaveData.onclick = () => {
        console.log(selectData.value)
    }

    btnUploadData.onclick = () => {
        $('#update-data-modal').modal('show')
    }

    btnUpload.onclick = () => {
        const zipFileInput = document.getElementById("zipFileInput");
        const zipFile = zipFileInput.files[0];

        fs.createReadStream(zipFile)
            .pipe(unzipper.Parse())
            .on("entry", function (entry) {
                const fileName = entry.path;
                const type = entry.type; // 'Directory' or 'File'
                const size = entry.vars.uncompressedSize; // The size of the uncompressed file

                if (type === "File") {
                    entry.pipe(fs.createWriteStream(`./json-files/${fileName}`));
                } else {
                    entry.autodrain();
                }
            });
    }

    ////////////////////////////////////////////////// Map and Map Layers

    return{}
})();
