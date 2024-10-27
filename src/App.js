import React, { useState } from 'react'; 
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import PathPage from './PathPage'; 

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [paths, setPaths] = useState([]);
  const [classCounts, setClassCounts] = useState({});
  
  const [x1, setX1] = useState('');
  const [x2, setX2] = useState('');
  const [y1, setY1] = useState('');
  const [y2, setY2] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleFolderChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      Array.from(files).forEach((file) => {
        uploadFile(file);
      });
    }
  };

  
  const classNames = [
    'Bunker', 'Cargo', 'Cistern', 'ClassCarriage', 'Dumpcar',
    'Fitting platorm', 'Halfcarriage', 'Laying crane', 'MTSO',
    'PRSM Machine', 'Platform PPK', 'SMMachine', 'Sapsan', 'USOPlatform'
  ];
  
  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
  
    formData.append('x1', x1);
    formData.append('x2', x2);
    formData.append('y1', y1);
    formData.append('y2', y2);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        setImageUrl(data.result_image);
        
        const namedClassCounts = {};
        for (const [classId, count] of Object.entries(data.class_counts)) {
          const className = classNames[parseInt(classId, 10)];
          namedClassCounts[className] = count;
        }
        setClassCounts(namedClassCounts);
      } else {
        const errorData = await response.json();
        console.error('Error uploading file:', errorData);
      }
    } catch (error) {
      console.error('Error during upload:', error);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    uploadFile(file);
  };

  const showGraph = () => {
    window.open('http://127.0.0.1:5000/show-image', '_blank');
  };

  const addPath = () => {
    const newPath = prompt('Введите имя нового пути:');
    if (newPath && !paths.includes(newPath)) {
      setPaths([...paths, newPath]);
    } else {
      alert('Путь уже существует или имя пустое.');
    }
  };

  const removePath = () => {
    const pathToRemove = prompt('Введите имя пути для удаления:');
    if (pathToRemove) {
      setPaths(paths.filter(path => path !== pathToRemove));
    } else {
      alert('Имя пути не может быть пустым.');
    }
  };

  return (
    <Router>
      <div className="App">
        <h1>pfo</h1>
        
        <input
          type="file"
          accept="video/*, image/*"
          onChange={handleFileChange}
        />
        {fileName && <p>Загруженный файл: {fileName}</p>}
        
        <button onClick={handleUpload}>Обработать</button>
        <button onClick={showGraph}>Показать график</button>

        <input
          type="file"
          webkitdirectory="true"
          multiple
          onChange={handleFolderChange}
        />
        <button onClick={addPath}>Добавить путь</button>
        <button onClick={removePath}>Удалить путь</button>
        
        <div>
          <h3>Список путей:</h3>
          {paths.length > 0 ? (
            paths.map((path, index) => (
              <Link key={index} to={`/ways/${path}`}>
                <button>{path}</button>
              </Link>
            ))
          ) : (
            <p>Нет добавленных путей.</p>
          )}
        </div>

        {imageUrl && (
          <div>
            <h3>Обработанное изображение:</h3>
            <img src={`http://127.0.0.1:5000${imageUrl}`} alt="Обработанное" />
          </div>
        )}

        {/* Поля ввода для координат */}
        <div>
          <h3>Координаты</h3>
          <label>
            x1:
            <input type="number" value={x1} onChange={(e) => setX1(e.target.value)} />
          </label>
          <label>
            x2:
            <input type="number" value={x2} onChange={(e) => setX2(e.target.value)} />
          </label>
          <label>
            y1:
            <input type="number" value={y1} onChange={(e) => setY1(e.target.value)} />
          </label>
          <label>
            y2:
            <input type="number" value={y2} onChange={(e) => setY2(e.target.value)} />
          </label>
        </div>

        {/* Таблица с двумя пустыми колонками */}
        <div>
          <h3>Данные</h3>
          <table>
            <thead>
              <tr>
                <th>Колонка 1</th>
                <th>Колонка 2</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td></td>
                <td></td>
              </tr>
              {/* Вы можете добавить больше строк по мере необходимости */}
            </tbody>
          </table>
        </div>

        {classCounts && Object.keys(classCounts).length > 0 && (
        <div>
          <h3>Результаты анализа</h3>
          <table>
            <thead>
              <tr>
                <th>Класс</th>
                <th>Количество</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(classCounts).map(([className, count], index) => (
                <tr key={index}>
                  <td>{className}</td>
                  <td>{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

        {/* Добавление маршрутов */}
        <Routes>
          <Route path="/ways/:pathName" element={<PathPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
