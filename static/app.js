const cards = document.querySelectorAll('.music-card');
let currentCardIndex = 0;
let isSwiping = false;

const card = cards[currentCardIndex];

// Start dragging
card.addEventListener('mousedown', (e) => {
    isSwiping = true;
    card.classList.add('moving');
});

// On mouse move, update the card's position
document.addEventListener('mousemove', (e) => {
    if (!isSwiping) return;

    const diff = e.clientX - card.getBoundingClientRect().left;
    card.style.transform = `translateX(${diff}px)`;  // Moves the card

    if (diff > 100) {
        card.classList.add('right'); // Swipe Right
    } else if (diff < -100) {
        card.classList.add('left'); // Swipe Left
    }
});

// End dragging and swipe the card
document.addEventListener('mouseup', () => {
    if (!isSwiping) return;

    isSwiping = false;

    // If card moved far enough, apply the appropriate action (right or left)
    if (card.style.transform.includes("translateX(100%)")) {
        // Right swipe (like the song, add to playlist)
        card.classList.add('fling-right');
        addToSpotifyPlaylist();
    } else if (card.style.transform.includes("translateX(-100%)")) {
        // Left swipe (dislike the song, don't add to playlist)
        card.classList.add('fling-left');
    }

    // Reset card position after fling
    setTimeout(() => {
        card.style.transform = 'translateX(0)';
        card.classList.remove('right', 'left', 'fling-right', 'fling-left');
        
        // Move to the next card in the stack
        currentCardIndex++;
        if (currentCardIndex >= cards.length) {
            currentCardIndex = 0;
        }

        const nextCard = cards[currentCardIndex];
        nextCard.style.transform = 'translateX(0)';
    }, 300);  // Wait for the fling animation to complete
});

// Click event for the Like Button
document.querySelector('.like-btn').addEventListener('click', () => {
    card.classList.add('fling-right');
    addToSpotifyPlaylist();
    resetCardPosition();
});

// Click event for the Dislike Button
document.querySelector('.dislike-btn').addEventListener('click', () => {
    card.classList.add('fling-left');
    resetCardPosition();
});

// Simulate adding the song to a Spotify playlist
function addToSpotifyPlaylist() {
    console.log('Song added to playlist!');
}

function resetCardPosition() {
    setTimeout(() => {
        card.style.transform = 'translateX(0)';
        card.classList.remove('fling-right', 'fling-left');
        
        // Move to the next card in the stack
        currentCardIndex++;
        if (currentCardIndex >= cards.length) {
            currentCardIndex = 0;
        }

        const nextCard = cards[currentCardIndex];
        nextCard.style.transform = 'translateX(0)';
    }, 300);  // Wait for the fling animation to complete
}



