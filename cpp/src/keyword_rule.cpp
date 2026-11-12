#include "keyword_rule.h"

#include <utility>

KeywordRule::KeywordRule(std::string keyword) : keyword_(std::move(keyword)) {}

bool KeywordRule::matches(const ArticleText& article) const {
    return article.text.find(keyword_) != std::string::npos;
}
