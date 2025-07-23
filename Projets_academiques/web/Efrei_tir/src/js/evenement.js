const upcomingEvents = [
    {
      activity: "Session de Tir à l'Arc US Villejuif",
      date: "2024-06-08",
      remainingSeats: 6,
      address: "44 ave Karl Marx 94800 Villejuif",
      imageUrl: "../img/Evenements/IMG_25002.jpg"
    },
    {
      activity: "Partie d'Airsoft chez Wild Trigger",
      date: "2024-06-15",
      remainingSeats: 22,
      address: "18 BIS Rue du Plateau, 92500 Rueil-Malmaison",
      imageUrl: "../img/Evenements/IMG_25000.jpg"
    },
    {
      activity: "Partie de Laser quest chez LaserGame",
      date: "2024-06-28",
      remainingSeats: 11,
      address: "Centre commercial, 94110 Arceuil",
      imageUrl: "../img/Evenements/IMG_25004.jpg"
    },
    {
      activity: "Partie d'Airsoft chez Les Gobelins de Mériel (en Grotte !)",
      date: "2024-05-18",
      remainingSeats: 2,
      address: "Rue de l'abbaye du val, 95630 Mériel",
      imageUrl: "../img/Evenements/IMG_25001.jpg"
    },
    {
      activity: "Session de Tir à l'Arc CAV Parisis",
      date: "2024-07-02",
      remainingSeats: 9,
      address: "11 Av. de la Prte de Choisy, 75013 Paris",
      imageUrl: "../img/Evenements/IMG_25003.jpg"
    },
    {
      activity: "Partie de Laser quest chez CosmicLaser",
      date: "2024-08-28",
      remainingSeats: 15,
      address: "3 rue des Alouettes, 94320 Thiais",
      imageUrl: "../img/Evenements/IMG_25005.jpg"
    }
  ];
  
  const upcomingEventsList = document.getElementById('upcomingEvents');
  
  upcomingEvents.forEach(event => {
    const eventItem = document.createElement('li');
    eventItem.classList.add('upcoming-event');
  
    const eventImage = document.createElement('img');
    eventImage.src = event.imageUrl;
    eventImage.classList.add('event-image');
    eventItem.appendChild(eventImage);
  
    const eventDetails = document.createElement('div');
    eventDetails.classList.add('event-details');

    const date = document.createElement('p');
    date.innerHTML = `<span class="label">Date:</span> ${event.date}`;
    eventDetails.appendChild(date);
  
    const activity = document.createElement('p');
    activity.innerHTML = `<span class="label">Activité:</span> ${event.activity}`;
    eventDetails.appendChild(activity);
  
    const seats = document.createElement('p');
    seats.innerHTML = `<span class="label">Places restantes:</span> ${event.remainingSeats}`;
    eventDetails.appendChild(seats);
  
    const address = document.createElement('p');
    address.innerHTML = `<span class="label">Adresse:</span> ${event.address}`;
    eventDetails.appendChild(address);
  
    const registerButton = document.createElement('button');
    registerButton.textContent = "S'inscrire";
    registerButton.classList.add('register-button');
    registerButton.addEventListener('click', () => {
      window.location.href = `inscription.html?activity=${encodeURIComponent(event.activity)}&date=${encodeURIComponent(event.date)}&location=${encodeURIComponent(event.address)}`;
    });
    eventDetails.appendChild(registerButton);
  
    eventItem.appendChild(eventDetails);
  
    upcomingEventsList.appendChild(eventItem);
  });
