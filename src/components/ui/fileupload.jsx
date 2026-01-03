import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const FileUpload = ({ label, accept, onChange, preview, id }) => {
  const [fileName, setFileName] = useState('');
  
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onChange(file);
    }
  };
  
  const inputId = id || `file-${label?.replace(/\s+/g, '-')}`;
  
  return (
    <div className="w-full">
      {label && <label className="block text-sm font-medium text-gray-700 mb-1.5">{label}</label>}
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
        <input
          type="file"
          accept={accept}
          onChange={handleChange}
          className="hidden"
          id={inputId}
        />
        <label htmlFor={inputId} className="cursor-pointer">
          <Upload className="mx-auto text-gray-400 mb-2" size={32} />
          <p className="text-sm text-gray-600">
            {fileName || 'Click to upload or drag and drop'}
          </p>
        </label>
      </div>
      {preview && (
        <div className="mt-4">
          {preview}
        </div>
      )}
    </div>
  );
};

export default FileUpload;