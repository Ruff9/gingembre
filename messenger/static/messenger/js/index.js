const current_user_id = JSON.parse(document.getElementById('current_user_id').textContent);
const api_url = window.location.origin + '/conversation_index/'
const setIntervalAsync = SetIntervalAsync.setIntervalAsync;


document.addEventListener('alpine:init', () => {
    Alpine.store('indexData', {
        conversations: {},
        showEmpty: false,

        get conversationCount () {
            return Object.keys(this.conversations).length
        },

        async init() {
            this.conversations = await getDataFromAPI();
            this.showEmpty = true;
        }
    })
})


async function getDataFromAPI() {
    const response = await fetch(api_url)
    return response.json()
}

async function updateData() {
    Alpine.store('indexData').conversations = await getDataFromAPI();
}

const timer = setIntervalAsync(async () => {
    await updateData()
}, 1000);
