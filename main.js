document.addEventListener('DOMContentLoaded', () => {
    const file1Input = document.getElementById('file-1');
    const file2Input = document.getElementById('file-2');
    const file1Info = document.getElementById('file-1-info');
    const file2Info = document.getElementById('file-2-info');
    const file1Cols = document.getElementById('file-1-cols');
    const file2Cols = document.getElementById('file-2-cols');
    const compareBtn = document.getElementById('compare-btn');
    const compareSection = document.getElementById('compare-section');

    let file1Data = null;
    let file2Data = null;

    async function uploadFile(file, side) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('side', side);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.error) {
                alert(data.error);
                return;
            }
            displayMetadata(data, side);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }

    function displayMetadata(data, side) {
        const infoDiv = document.getElementById(`file-${side}-info`);
        const colSelect = document.getElementById(`file-${side}-cols`);
        
        let html = '';
        data.sheets.forEach(sheet => {
            html += `<div><strong>الشيت:</strong> ${sheet.name} | <strong>الصفوف:</strong> ${sheet.rows} | <strong>الاعمدة:</strong> ${sheet.cols}</div>`;
        });
        infoDiv.innerHTML = html;

        colSelect.innerHTML = '<option value="">اختر عمود المقارنة الأساسي</option>';
        data.columns.forEach(col => {
            const option = document.createElement('option');
            option.value = col;
            option.textContent = col;
            colSelect.appendChild(option);
        });
        colSelect.style.display = 'block';

        if (side === '1') file1Data = data;
        if (side === '2') file2Data = data;

        if (file1Data && file2Data) {
            compareSection.style.display = 'block';
        }
    }

    file1Input.addEventListener('change', (e) => {
        if (e.target.files[0]) uploadFile(e.target.files[0], '1');
    });

    file2Input.addEventListener('change', (e) => {
        if (e.target.files[0]) uploadFile(e.target.files[0], '2');
    });

    compareBtn.addEventListener('click', async () => {
        const col1 = file1Cols.value;
        const col2 = file2Cols.value;

        if (!col1 || !col2) {
            alert('يرجى اختيار الاعمدة للمقارنة');
            return;
        }

        const formData = new FormData();
        formData.append('file1_id', file1Data.file_id);
        formData.append('file2_id', file2Data.file_id);
        formData.append('col1', col1);
        formData.append('col2', col2);

        try {
            const response = await fetch('/compare', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.download_url) {
                const downloadSection = document.getElementById('download-section');
                const downloadLink = document.getElementById('download-link');
                downloadLink.href = data.download_url;
                downloadSection.style.display = 'block';
            }
        } catch (error) {
            console.error('Error comparing files:', error);
        }
    });
});
