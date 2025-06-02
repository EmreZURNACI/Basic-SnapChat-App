import React, { useEffect, useState } from "react";
import { Alert, TouchableOpacity, ActivityIndicator } from "react-native";
import { useDispatch, useSelector } from "react-redux";
import { setImage } from "../redux/ImageSlice";
import { View, Text, Image, ScrollView } from "dripsy";
import * as ImagePicker from "expo-image-picker";

export default function HomeScreen() {
  const dispatch = useDispatch();
  const imageUri = useSelector((state) => state.image.uri);

  const [imageList, setImageList] = useState([
    "https://e7.pngegg.com/pngimages/662/1004/png-clipart-glasses-glasses.png",
    "https://e7.pngegg.com/pngimages/847/198/png-clipart-sunglasses-sunglasses-thumbnail.png",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZ5RS-b2QS5iwti_Z3WnIfZdzxOXowdi6eQA&s",
    "https://w7.pngwing.com/pngs/281/222/png-transparent-humanoid-robot-telegram-robocup-robot-electronics-sticker-humanoid-robot-thumbnail.png",
    "https://e7.pngegg.com/pngimages/998/59/png-clipart-mirror-mirror.png",
    "https://w7.pngwing.com/pngs/623/242/png-transparent-eyes-and-eyebrows-illustration-eye-cartoon-computer-file-creative-cartoon-eyes-cartoon-character-blue-people-thumbnail.png",
    "https://e7.pngegg.com/pngimages/111/884/png-clipart-graphics-cartoon-drawing-person-with-binoculars-hand-vertebrate.png",
    "https://w7.pngwing.com/pngs/490/614/png-transparent-fedora-hat-cap-beanie-beret-hats-hat-fashion-cowboy-hat.png",
    "https://e7.pngegg.com/pngimages/776/375/png-clipart-moustache-moustache.png",
    "https://w7.pngwing.com/pngs/910/545/png-transparent-heart-pixel-art-pixel-flag-text-symmetry-thumbnail.png",
  ]);

  const [paths, setPaths] = useState([
    "gozluk",
    "gunesgozluk",
    "spiral",
    "robot",
    "yansima",
    "gozbalon",
    "karikatur",
    "sapka",
    "biyik",
    "piksel",
  ]);
  const [isLoading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(null);

  useEffect(() => {
    (async () => {
      const { status: mediaStatus } =
        await ImagePicker.requestMediaLibraryPermissionsAsync();
      const { status: cameraStatus } =
        await ImagePicker.requestCameraPermissionsAsync();

      if (mediaStatus !== "granted" || cameraStatus !== "granted") {
        Alert.alert(
          "İzin Gerekli",
          "Uygulamanın çalışması için izin vermelisiniz."
        );
      }
    })();
  }, []);

  const handleSelectImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!result.canceled) {
      dispatch(setImage(result.assets[0].uri));
    }
  };

  const handleTakePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!result.canceled) {
      dispatch(setImage(result.assets[0].uri));
    }
  };

  const handleSend = async () => {
    if (!imageUri) {
      alert("Lütfen önce bir resim seçin.");
      return;
    }

    const formData = new FormData();
    formData.append("file", {
      uri: imageUri,
      name: "photo.jpg",
      type: "image/jpeg",
    });

    try {
      setLoading(true);
      const response = await fetch(
        `http://192.168.1.85:5000/${paths[selectedIndex]}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "multipart/form-data",
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(`Sunucu hatası: ${response.status}`);
      }

      const data = await response.json();

      // Base64 döndüyse bunu URI olarak birleştir
      const base64Image = `data:image/png;base64,${data.image_base64}`;
      dispatch(setImage(base64Image));
    } catch (error) {
      console.error("Gönderim hatası:", error);
      alert("Gönderim sırasında hata oluştu: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  // JSX Return
  if (isLoading) {
    return (
      <View sx={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" color="#2563eb" />
        <Text sx={{ mt: 3 }}>Yükleniyor...</Text>
      </View>
    );
  }

  return (
    <View sx={{ flex: 1, backgroundColor: "background" }}>
      {/* ÜST: GÖRSEL */}
      <View sx={{ flex: 1 }}>
        {imageUri ? (
          <Image
            source={{ uri: imageUri }}
            style={{ flex: 1, width: "100%" }}
            resizeMode="cover"
          />
        ) : (
          <View
            style={{
              flex: 1,
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "background",
            }}
          >
            <Text sx={{ variant: "text.gray500", fontSize: 18 }}>
              Görsel seçilmedi
            </Text>
          </View>
        )}
      </View>

      {/* ORTA: THUMBNAILLAR */}
      <View
        style={{
          position: "absolute",
          bottom: 50,
          left: 0,
          right: 0,
          flexDirection: "row",
          justifyContent: "space-around",
          backgroundColor: "#fff", // Gölge etkisi için gerekli
          borderTopWidth: 1,
          borderColor: "#e5e5e5",
        }}
      >
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{
            flexDirection: "row",
            alignItems: "center",
            paddingHorizontal: 8,
            paddingVertical: 8,
            bottom: 1,
            left: 0,
            border: 1,
            right: 0,
          }}
          style={{
            width: "100%",
            backgroundColor: "background",
          }}
        >
          {imageList.map((uri, index) => (
            <TouchableOpacity
              key={index}
              onPress={() => setSelectedIndex(index)}
              style={{
                marginHorizontal: 8,
                width: 65,
                height: 65,
                borderRadius: 32.5,
                borderWidth: 3,
                borderColor: selectedIndex === index ? "#2563eb" : "#ccc",
                padding: 2,
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Image
                source={{ uri }}
                style={{
                  width: 60,
                  height: 60,
                  borderRadius: 30,
                }}
              />
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* ALT: BUTONLAR - Sabitlenmiş */}
      <View
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          flexDirection: "row",
          justifyContent: "space-around",
          paddingVertical: 12,
          backgroundColor: "#fff", // Gölge etkisi için gerekli
          borderTopWidth: 1,
          borderColor: "#e5e5e5",
        }}
      >
        <TouchableOpacity
          onPress={handleSelectImage}
          style={{
            backgroundColor: "#2563eb",
            paddingVertical: 12,
            paddingHorizontal: 15,
            borderRadius: 16,
            width: 110,
            alignItems: "center",
          }}
        >
          <Text sx={{ variant: "text.semiboldWhite" }}>Galeriden Seç</Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={handleTakePhoto}
          style={{
            backgroundColor: "#16a34a",
            paddingVertical: 12,
            paddingHorizontal: 15,
            borderRadius: 16,
            width: 110,
            alignItems: "center",
          }}
        >
          <Text sx={{ variant: "text.semiboldWhite" }}>Fotoğraf Çek</Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={handleSend}
          style={{
            backgroundColor: "#ef4444",
            paddingVertical: 12,
            paddingHorizontal: 15,
            borderRadius: 16,
            width: 110,
            alignItems: "center",
          }}
        >
          <Text sx={{ variant: "text.semiboldWhite" }}>Gönder</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
