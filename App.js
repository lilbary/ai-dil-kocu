import React, { useState } from 'react';
import LoginScreen from './src/screens/LoginScreen'; // Yolunu kontrol et


export default function App() {
  const [token, setToken] = useState(null);

  // Eğer token varsa Home'u, yoksa Login'i göster
  if (token) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text>Giriş Başarılı! Burası Home Ekranı Olacak.</Text>
      </View>
    );
  }

  return (
    <LoginScreen 
      onLoginSuccess={(newToken) => {
        console.log("App.js: Token geldi kanka!", newToken);
        setToken(newToken); // İşte burası o eksik olan fonksiyon!
      }} 
    />
  );
}