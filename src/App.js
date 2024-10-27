import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const handleImageChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile); 
      setFileName(selectedFile.name);
    }
  };

  const handleUpload = async () => {
    if (!file) return; 
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        setImageUrl(data.result_image); // Сохранение URL результата
      } else {
        const errorData = await response.json();
        console.error('Error uploading file:', errorData);
      }
    } catch (error) {
      console.error('Error during upload:', error);
    }
  };
  

  const showGraph = () => {
    window.open('http://127.0.0.1:5000/show-image', '_blank');
  };

  return (
    <div className="App">
      <h1>pfo</h1>
      
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />
      {fileName && <p>Загруженный файл: {fileName}</p>}
      
      <button onClick={handleUpload}>Обработать</button>
      <button onClick={showGraph}>Показать график</button>
  
      {imageUrl && (
        <div>
          <h3>Обработанное изображение:</h3>
          <img src={`http://127.0.0.1:5000${imageUrl}`} alt="Обработанное" />
        </div>
      )}
    </div>
  );
}

export default App;

