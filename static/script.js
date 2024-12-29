document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("mainform");
    const htmlresult = document.getElementById("result")

    async function loadContent(url) {
        try {
            const response = await fetch(`partials/${url}.html`);
            if (!response.ok) throw new Error(`Errore nel caricamento: ${response.statusText}`);
            const html = await response.text();
            content.innerHTML = html;
        } catch (error) {
            content.innerHTML = `<p>Errore: ${error.message}</p>`;
        }
    }

    document.querySelectorAll("[data-link]").forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const pageName = event.target.getAttribute("href").split("/").pop().replace(".html", "");
            window.location.hash = pageName;
            htmlresult.innerHTML = ''
            htmlresult.style.display = 'none';
        });
    });

    function handleHashChange() {
        const pageName = window.location.hash.slice(1) || "PBKDF2-SHA256";
        loadContent(pageName);
    }

    window.addEventListener("hashchange", handleHashChange);

    handleHashChange();

    document.getElementById('mainform').addEventListener('submit', async (e) => {
        e.preventDefault()
    
        const formData = new FormData(e.target);
    
        const formDataObject = Object.fromEntries(formData.entries());
        const data = JSON.stringify(formDataObject)

        
        htmlresult.classList.add("blink")
        htmlresult.textContent = "thinking";
        htmlresult.style.display = 'block';
        let result
        const urlEndpoint = (formDataObject.urlEndpoint) ? formDataObject.urlEndpoint : 'encode'
        try {
            const response = await fetch(`/api/${urlEndpoint}/${formDataObject.algo}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: data
            });
    
            if (!response.ok) {
                throw new Error(`Errore HTTP: ${response.status}`);
            }
    
            const resp = await response.json()
            console.log(resp)
            result = resp.result
        } catch (error) {
            result = error.toString()
            console.error('Error:', error);
        }
        htmlresult.classList.remove("blink")
        htmlresult.innerHTML = result
    });    
});