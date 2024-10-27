self.onmessage = (e) => {
    const file = e.data;
    importScripts('https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js');
    Papa.parse(file, {
        header: true,
        complete: (result) => {
            self.postMessage(result.data);
        }
    });
};
