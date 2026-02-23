/** @type {import('internal-linking').LinkingConfig} */
export default {
  siteName: 'ProTrainerPrep',
  siteUrl: 'https://protrainerprep.com',
  distDir: './dist',
  pageTypes: [
    { name: 'pillar', pattern: /^\/career\/how-to-become/, role: 'pillar', minLinksOut: 8, maxLinksOut: 20 },
    { name: 'hub-guide', pattern: /\/(fitness-certification-guide|career-change-fitness-guide|career-building-guide|career-growth-guide)\/$/, role: 'hub', minLinksOut: 8, maxLinksOut: 15 },
    { name: 'spoke', pattern: /^\/(certifications|career-change|career-building|career-growth)\//, role: 'spoke', minLinksOut: 3, maxLinksOut: 8 },
    { name: 'category', pattern: /^\/category\//, role: 'static' },  // category pages are auto-generated, skip
    { name: 'tag', pattern: /^\/tag\//, role: 'static' },
    { name: 'blog-index', pattern: /^\/blog\//, role: 'static' },  // paginated index, skip
    { name: 'homepage', pattern: /^\/$/, role: 'static' },
    { name: 'static', pattern: /^\/(about|privacy|terms|affiliate-disclosure|thank-you)\/$/, role: 'static' },
  ],
  excludePaths: [/^\/404\//, /^\/decapcms\//, /^\/_astro\//, /^\/rss/, /^\/tag\//, /^\/category\//, /^\/blog\//],
  bodySelector: 'article, main',
  excludeSelectors: ['nav', 'header', 'footer', '.breadcrumb', '.related-posts', '[class*="RelatedPosts"]'],
  clusterStrategy: 'category-slug',
  dataDir: 'src/data/post',
};
