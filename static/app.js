const cardsContainer = document.querySelector('.music-card-container');
const iframe = document.getElementById('spotify-player');
const likeBtn = document.querySelector('.like-btn');
const dislikeBtn = document.querySelector('.dislike-btn');

let currentCardIndex = 0;

// Function to fetch artist info and create a music card
async function fetchRandomMusicCard() {
    try {
        const response = await fetch('/get_artist_info');
        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        const { artist_name, artist_image, track_id, track_name } = data;

        // Create and display the new music card
        const newCard = createMusicCard(artist_name, track_name, track_id, artist_image);
        cardsContainer.appendChild(newCard);

        // Show the first card
        if (cardsContainer.children.length === 1) {
            showCard(currentCardIndex);
        }

    } catch (error) {
        console.error("Error fetching artist data:", error);
    }
}

// Function to create a music card
function createMusicCard(artistName, trackName, trackId, artistImageUrl) {
    const card = document.createElement('div');
    card.classList.add('music-card');
    card.style.display = 'none'; // Initially hidden

    const cardImage = document.createElement('img');
    cardImage.src = artistImageUrl;
    cardImage.alt = `${artistName} - ${trackName}`;

    const cardTitle = document.createElement('h3');
    cardTitle.textContent = trackName;

    const cardArtist = document.createElement('p');
    cardArtist.textContent = artistName;

    const playButton = document.createElement('button');
    playButton.textContent = "Play Song";
    playButton.addEventListener('click', () => {
        iframe.src = `https://open.spotify.com/embed/track/${trackId}`;
        iframe.style.display = "block";
    });

    card.appendChild(cardImage);
    card.appendChild(cardTitle);
    card.appendChild(cardArtist);
    card.appendChild(playButton);

    return card;
}

// Function to show a specific card
function showCard(index) {
    const cards = document.querySelectorAll('.music-card');
    if (cards.length === 0) return;

    // Hide all cards
    cards.forEach(card => card.style.display = 'none');

    // Show the current card
    cards[index].style.display = 'block';
}

// Function to handle like/dislike actions
function handleAction(direction) {
    const cards = document.querySelectorAll('.music-card');
    if (cards.length === 0) return;

    // Apply swipe animation
    cards[currentCardIndex].classList.add(direction);
    setTimeout(() => {
        cards[currentCardIndex].remove();
        currentCardIndex = 0; // Reset to the first card
        showCard(currentCardIndex);

        // Fetch a new card after swiping
        fetchRandomMusicCard();
    }, 300);
}

// Event listeners for like/dislike buttons
likeBtn.addEventListener('click', () => handleAction('right'));
dislikeBtn.addEventListener('click', () => handleAction('left'));

// Initial fetch and load cards
fetchRandomMusicCard();