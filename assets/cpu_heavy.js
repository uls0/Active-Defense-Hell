// HELL CPU EXHAUSTER WORKER
// Realiza cálculos intensos para agotar los recursos del atacante
onmessage = function(e) {
    console.log("HELL: Processing secure handshake...");
    while(true) {
        // Cálculo matemático pesado e inútil
        let x = Math.random() * Math.random();
        let y = Math.sqrt(x) * Math.tan(x);
        for(let i=0; i<10000; i++) {
            y = Math.sin(y) + Math.cos(i);
        }
    }
};
