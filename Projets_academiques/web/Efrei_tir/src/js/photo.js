const events = [
  {
      name: "Partie d'Airsoft chez Max2Joules",
      date: "2023-05-20",
      photos: ['../img/Airsoft 1/IMG_2293.JPEG', '../img/Airsoft 1/IMG_2294.JPEG', '../img/Airsoft 1/IMG_2296.JPEG', '../img/Airsoft 1/IMG_2299.JPEG']
  },
  {
      name: "Partie d'Airsoft chez Les Gobelins de Mériel",
      date: "2023-07-12",
      photos: ['../img/Airsoft 2/IMG_2292.JPEG', '../img/Airsoft 2/IMG_2297.JPEG', '../img/Airsoft 2/IMG_2298.JPEG']
  },
  {
      name: "Partie d'Airsoft chez Médicine",
      date: "2024-02-24",
      photos: ['../img/Airsoft 3/IMG_2306.JPEG', '../img/Airsoft 3/IMG_2307.JPEG', '../img/Airsoft 3/IMG_2308.JPEG', '../img/Airsoft 3/IMG_2309.JPEG', '../img/Airsoft 3/IMG_2310.JPEG', '../img/Airsoft 3/IMG_2312.JPEG']
  },
  {
      name: "Session de Tir à l'Arc chez USV",
      date: "2023-10-01",
      photos: ['../img/Tir arc 1/IMG_2300.JPEG', '../img/Tir arc 1/IMG_2301.JPEG', '../img/Tir arc 1/IMG_2302.JPEG', '../img/Tir arc 1/IMG_2303.JPEG', '../img/Tir arc 1/IMG_2304.JPEG', '../img/Tir arc 1/IMG_2305.JPEG']
  },
  {
      name: "Session de préparation à la compétition de Tir à l'Arc",
      date: "2024-03-26",
      photos: ['../img/Tir arc 2/IMG_2400.jpg', '../img/Tir arc 2/IMG_2401.jpg', '../img/Tir arc 2/IMG_2402.jpg', '../img/Tir arc 2/IMG_2403.jpg']
  }
];

const eventList = document.getElementById('eventList');

events.forEach(event => {
  const eventItem = document.createElement('li');
  eventItem.classList.add('event');

  const eventTitle = document.createElement('h2');
  eventTitle.textContent = `${event.name} - ${event.date}`;
  eventItem.appendChild(eventTitle);

  const photoStrip = document.createElement('div');
  photoStrip.classList.add('photo-strip');

  for (let i = 0; i < 3 && i < event.photos.length; i++) {
      const img = document.createElement('img');
      img.src = event.photos[i];
      img.classList.add('strip-photo');
      photoStrip.appendChild(img);
  }

  eventItem.appendChild(photoStrip);
  eventList.appendChild(eventItem);

  let currentIndex = 0;

  setInterval(() => {
      currentIndex = (currentIndex + 1) % event.photos.length;
      const nextIndex = (currentIndex + 3) % event.photos.length;

      const img = document.createElement('img');
      img.src = event.photos[nextIndex];
      img.classList.add('strip-photo');

      photoStrip.removeChild(photoStrip.firstChild);
      photoStrip.appendChild(img);
  }, 3000); //Temps de défilement tu peux le modifier 3 sec c'est pas mal
});
