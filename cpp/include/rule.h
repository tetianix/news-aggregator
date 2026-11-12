#pragma once

#include <string>

struct ArticleText {
    std::string id;
    std::string text;
};

class Rule {
public:
    virtual ~Rule() = default;
    virtual bool matches(const ArticleText& article) const = 0;
};
