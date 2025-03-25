const form = document.querySelector('form');
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const loadingIndicator = document.getElementById('loading');

form.onsubmit = async function(event) {
    event.preventDefault();

    progressBarContainer.style.display = 'block';  // プログレスバーを表示
    loadingIndicator.style.display = 'block';  // ローディングインジケーターを表示

    const formData = new FormData(form);

    // アップロードの進行状況を追跡するためにfetchの進行状況イベントを使用
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        },
        onprogress: (event) => {
            if (event.lengthComputable) {
                const percent = (event.loaded / event.total) * 100;
                progressBar.value = percent;  // プログレスバーを更新
            }
        }
    });

    const result = await response.json();
    if (response.ok) {
        transcriptionLink.href = '/download/' + result.transcription_file;
        downloadLink.style.display = 'block';
    } else {
        messageElement.textContent = "Error: " + result.error;
    }

    // 完了後に表示を更新
    progressBarContainer.style.display = 'none';
    loadingIndicator.style.display = 'none';
};
