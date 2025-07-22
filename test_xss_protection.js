// XSS Protection Test Script
// This script tests the sanitization functions from register.html

console.log('🎯 TESTING XSS PROTECTION FUNCTIONS');

// Copy the sanitization functions from register.html
function sanitizeInput(input) {
    // Nettoie les entrées utilisateur contre XSS côté frontend
    if (typeof input !== 'string') return input;
    
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/javascript:/gi, '')
        .replace(/on\w+\s*=/gi, '')
        .trim();
}

function sanitizeFormData(data) {
    // Nettoie toutes les données du formulaire
    const cleaned = {};
    for (const [key, value] of Object.entries(data)) {
        if (typeof value === 'string') {
            cleaned[key] = sanitizeInput(value);
        } else {
            cleaned[key] = value;
        }
    }
    return cleaned;
}

// Test XSS payloads as specified in the review request
console.log('\n🔒 PHASE 1: TESTING XSS PAYLOADS');

const xssPayloads = {
    firstName: "<script>alert('XSS_FIRSTNAME')</script>",
    lastName: "<img src=x onerror=alert('XSS_LASTNAME')>",
    email: "test@example.com",
    phone: "+596123456789",
    password: "SecurePass123!",
    birthDate: "1990-01-01",
    nationality: "FR",
    terms: true
};

console.log('Original data with XSS payloads:');
console.log(JSON.stringify(xssPayloads, null, 2));

// Apply sanitization
const sanitizedData = sanitizeFormData(xssPayloads);

console.log('\n🔒 PHASE 2: SANITIZED DATA');
console.log('🔒 Données sanitisées:', JSON.stringify(sanitizedData, null, 2));

// Verify XSS protection
console.log('\n🔒 PHASE 3: VERIFICATION');

const expectedResults = {
    firstName: "&amp;lt;script&amp;gt;alert('XSS_FIRSTNAME')&amp;lt;/script&amp;gt;",
    lastName: "&amp;lt;img src=x onerror=alert('XSS_LASTNAME')&amp;gt;"
};

let xssProtectionWorking = true;

// Check firstName sanitization
if (sanitizedData.firstName.includes('&lt;script&gt;') && sanitizedData.firstName.includes('&lt;/script&gt;')) {
    console.log('✅ firstName XSS payload properly escaped: <script> → &lt;script&gt;');
} else {
    console.log('❌ firstName XSS payload NOT properly escaped');
    xssProtectionWorking = false;
}

// Check lastName sanitization  
if (sanitizedData.lastName.includes('&lt;img') && sanitizedData.lastName.includes('&gt;')) {
    console.log('✅ lastName XSS payload properly escaped: <img> → &lt;img&gt;');
} else {
    console.log('❌ lastName XSS payload NOT properly escaped');
    xssProtectionWorking = false;
}

// Check that no dangerous characters remain
const dangerousChars = ['<script>', '<img', 'onerror=', 'javascript:'];
let foundDangerous = false;

for (const [key, value] of Object.entries(sanitizedData)) {
    if (typeof value === 'string') {
        for (const dangerous of dangerousChars) {
            if (value.toLowerCase().includes(dangerous.toLowerCase())) {
                console.log(`❌ Dangerous pattern "${dangerous}" found in ${key}: ${value}`);
                foundDangerous = true;
                xssProtectionWorking = false;
            }
        }
    }
}

if (!foundDangerous) {
    console.log('✅ No dangerous XSS patterns found in sanitized data');
}

console.log('\n🔒 PHASE 4: TESTING CLEAN DATA');

const cleanData = {
    firstName: "Marie-Claire",
    lastName: "Dubois",
    email: "marie.dubois@example.com",
    phone: "+596123456789",
    password: "SecurePass123!",
    birthDate: "1990-01-01",
    nationality: "FR",
    terms: true
};

const sanitizedCleanData = sanitizeFormData(cleanData);
console.log('Clean data after sanitization:', JSON.stringify(sanitizedCleanData, null, 2));

// Verify clean data is preserved
let cleanDataPreserved = true;
for (const [key, value] of Object.entries(cleanData)) {
    if (typeof value === 'string' && sanitizedCleanData[key] !== value) {
        console.log(`⚠️ Clean data modified for ${key}: "${value}" → "${sanitizedCleanData[key]}"`);
        cleanDataPreserved = false;
    }
}

if (cleanDataPreserved) {
    console.log('✅ Clean data preserved correctly');
}

console.log('\n🎯 FINAL RESULTS:');
console.log(`XSS Protection Status: ${xssProtectionWorking ? '✅ WORKING' : '❌ FAILED'}`);
console.log(`Clean Data Preservation: ${cleanDataPreserved ? '✅ WORKING' : '❌ FAILED'}`);

if (xssProtectionWorking && cleanDataPreserved) {
    console.log('\n🎉 XSS PROTECTION TEST PASSED - All security measures working correctly!');
} else {
    console.log('\n❌ XSS PROTECTION TEST FAILED - Security issues detected!');
}