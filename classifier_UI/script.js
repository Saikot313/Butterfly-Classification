
    const emojis = ['🦋', '🌸', '🍃', '🌿', '🌺', '✨'];
    const floaters = document.getElementById('floaters');
    for (let i = 0; i < 18; i++) {
            const el = document.createElement('div');
    el.className = 'floater';
    el.textContent = emojis[i % emojis.length];
    el.style.cssText = `
    left: ${Math.random() * 100}%;
    animation-duration: ${12 + Math.random() * 20}s;
    animation-delay: ${-Math.random() * 25}s;
    font-size: ${.8 + Math.random() * .9}rem;
    `;
    floaters.appendChild(el);
        }

    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const prevSect = document.getElementById('previewSection');
    const prevImg = document.getElementById('previewImg');
    const imgMeta = document.getElementById('imgMeta');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const spinner = document.getElementById('spinner');
    const btnText = document.getElementById('btnText');
    const errorBox = document.getElementById('errorBox');
    const errorMsg = document.getElementById('errorMsg');
    const resultCard = document.getElementById('resultCard');
    const resetBtn = document.getElementById('resetBtn');

    let selectedFile = null;

        dropZone.addEventListener('dragover', e => {e.preventDefault(); dropZone.classList.add('drag-over'); });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
        dropZone.addEventListener('drop', e => {
        e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) handleFile(file);
        });
        fileInput.addEventListener('change', () => {
            if (fileInput.files[0]) handleFile(fileInput.files[0]);
        });

    function handleFile(file) {
        selectedFile = file;
    const reader = new FileReader();
            reader.onload = e => {
        prevImg.src = e.target.result;
    prevSect.classList.add('show');
    const img = new Image();
                img.onload = () => {
        imgMeta.innerHTML = `
          <strong>Name:</strong> ${file.name}<br>
          <strong>Size:</strong> ${(file.size / 1024).toFixed(1)} KB<br>
          <strong>Dimensions:</strong> ${img.width} × ${img.height}<br>
          <strong>Type:</strong> ${file.type}
        `;
                };
    img.src = e.target.result;
            };
    reader.readAsDataURL(file);
    analyzeBtn.disabled = false;
    resultCard.classList.remove('show');
    hideError();
        }

        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
    setLoading(true);
    hideError();
    resultCard.classList.remove('show');

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
                const res = await fetch('/predict', {method: 'POST', body: formData });
    const data = await res.json();

    if (!data.success) {
        showError(data.error || 'Prediction failed.');
    return;
                }

    renderResults(data);
            } catch (err) {
        showError('Network error. Make sure Flask app is running.');
            } finally {
        setLoading(false);
            }
        });

    function renderResults(data) {
            const top = data.top_prediction;
    document.getElementById('topSpecies').textContent = top.species;
    document.getElementById('confText').textContent = `${top.confidence.toFixed(1)}% confidence`;

    const bars = document.getElementById('predBars');
    bars.innerHTML = '';
            data.predictions.forEach((p, i) => {
                const div = document.createElement('div');
    div.className = 'pred-row';
    div.innerHTML = `
    <div class="pred-label">
        <span class="pred-name">${i === 0 ? '🥇 ' : i === 1 ? '🥈 ' : '🥉 '}${p.species}</span>
        <span class="pred-pct">${p.confidence.toFixed(1)}%</span>
    </div>
    <div class="pred-bar-bg">
        <div class="pred-bar-fill${i > 0 ? ' secondary' : ''}" data-w="${p.confidence}"></div>
    </div>
    `;
    bars.appendChild(div);
            });

    document.getElementById('funFactText').textContent = data.fun_fact;
    resultCard.classList.add('show');

            setTimeout(() => {
        document.querySelectorAll('.pred-bar-fill').forEach(el => {
            el.style.width = el.dataset.w + '%';
        });
            }, 100);

    // Scroll to results
    resultCard.scrollIntoView({behavior: 'smooth', block: 'start' });
        }

        resetBtn.addEventListener('click', () => {
        selectedFile = null;
    fileInput.value = '';
    prevImg.src = '';
    prevSect.classList.remove('show');
    analyzeBtn.disabled = true;
    resultCard.classList.remove('show');
    hideError();
    window.scrollTo({top: 0, behavior: 'smooth' });
        });

    function setLoading(on) {
        analyzeBtn.disabled = on;
    spinner.style.display = on ? 'block' : 'none';
    btnText.textContent = on ? 'Analyzing...' : '🔍 Identify Butterfly';
        }
    function showError(msg) {
        errorMsg.textContent = msg;
    errorBox.classList.add('show');
        }
    function hideError() {
        errorBox.classList.remove('show');
        }
